from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import GPT, TimeSeriesPoint
from django.views.decorators.csrf import csrf_exempt
import datetime
import pytz

@csrf_exempt
def get_models(request):
    models = GPT.objects.all().values('id', 'slug')
    return JsonResponse(list(models), safe=False)

@csrf_exempt
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

@csrf_exempt
def update_download(request, id):
    model = get_object_or_404(GPT, id=id)
    current_date = datetime.datetime.now(pytz.utc).date()
    time_series_point, created = model.activitySummary.downloads.get_or_create(date=current_date, defaults={'count': 1})
    if not created:
        time_series_point.count += 1
        time_series_point.save()
    return JsonResponse({'message': 'Download count updated successfully'})

@csrf_exempt
def update_view(request, id):
    model = get_object_or_404(GPT, id=id)
    current_date = datetime.datetime.now(pytz.utc).date()
    time_series_point, created = model.activitySummary.views.get_or_create(date=current_date, defaults={'count': 1})
    if not created:
        time_series_point.count += 1
        time_series_point.save()
    return JsonResponse({'message': 'View count updated successfully'})
