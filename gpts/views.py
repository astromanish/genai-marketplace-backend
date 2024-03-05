from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import GPT, TimeSeriesPoint

def get_models(request):
    models = GPT.objects.all().values('id', 'slug')
    return JsonResponse(list(models), safe=False)

def get_model_details(request, id):
    model = get_object_or_404(GPT, id=id)
    context = {
        'id': model.id,
        'slug': model.slug,
        'owner_id': model.owner.id if model.owner else None,
        'owner_slug': model.owner.slug if model.owner else None,
        'description': model.description,
        'generated_date': model.activitySummary.generatedDate if model.activitySummary else None,
        'category_tags': [tag.name for tag in model.categories.tags.all()] if model.categories else [],
        'frameworks': model.frameworks,
        'downloads': [{'date': point.date, 'count': point.count} for point in model.activitySummary.downloads.all()],
        'views': [{'date': point.date, 'count': point.count} for point in model.activitySummary.views.all()]
    }
    return JsonResponse(context, safe=False)

def update_download(request, id):
    model = get_object_or_404(GPT, id=id)
    model.activitySummary.downloads.add(TimeSeriesPoint.objects.create(date=timezone.now(), count=1))
    return JsonResponse({'message': 'Download count updated successfully'})

def update_view(request, id):
    model = get_object_or_404(GPT, id=id)
    model.activitySummary.views.add(TimeSeriesPoint.objects.create(date=timezone.now(), count=1))
    return JsonResponse({'message': 'View count updated successfully'})
