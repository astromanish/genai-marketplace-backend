from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import GPT, Owner, ActivitySummary, Tags
from .serializers import GPTSerializer
from django.views.decorators.csrf import csrf_exempt
import datetime
import pytz

@csrf_exempt
def get_models(request):
    models = GPT.objects.all().values('id', 'slug', 'description', 'featured','tryitout_link', 'frameworks', 'tags__name')
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
        'generated_date': model.generatedDate,
        'tags': [tag.name for tag in model.tags.all()],
        'frameworks': model.frameworks,
        'upvotes': [{'date': point.date, 'count': point.count} for point in model.activitySummary.upvotes.all()],
        'views': [{'date': point.date, 'count': point.count} for point in model.activitySummary.views.all()],
        'featured': model.featured,
        'tryitout_link': model.tryitout_link
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def update_upvote(request, id):
    model = get_object_or_404(GPT, id=id)
    current_date = datetime.datetime.now(pytz.utc).date()
    time_series_point, created = model.activitySummary.upvotes.get_or_create(date=current_date, defaults={'count': 1})
    if not created:
        time_series_point.count += 1
        time_series_point.save()
    return JsonResponse({'message': 'Upvote count updated successfully'})

@csrf_exempt
def update_view(request, id):
    model = get_object_or_404(GPT, id=id)
    current_date = datetime.datetime.now(pytz.utc).date()
    time_series_point, created = model.activitySummary.views.get_or_create(date=current_date, defaults={'count': 1})
    if not created:
        time_series_point.count += 1
        time_series_point.save()
    return JsonResponse({'message': 'View count updated successfully'})

@csrf_exempt
def add_gpt_model(request):
    current_date = datetime.datetime.now(pytz.utc).date()
    if request.method == 'POST':
        
        data = request.POST.copy()

        activity_summary = ActivitySummary.objects.create()
        activity_summary.views.create(date=current_date, count=1)
        activity_summary.upvotes.create(date=current_date, count=1)

        owner_id = data.get('owner_id')
        owner = Owner.objects.get(id=owner_id) if owner_id else None

        tag_ids = data.getlist('tag_ids')
        tags = Tags.objects.filter(id__in=tag_ids)

        gpt_data = {
            'slug': data.get('slug', ''),
            'owner': owner,  
            'description': data.get('description', ''),
            'generatedDate': current_date,  # Change to 'generatedDate' to match model field name
            'activitySummary': activity_summary,
            'tags': tags,  
            'frameworks': data.get('frameworks'),
            'featured': data.get('featured', False),
            'tryitout_link': data.get('tryitout_link', ''),
        }
        
        serializer = GPTSerializer(data=gpt_data)
        
        if serializer.is_valid():
            instance = serializer.save()
            model = get_object_or_404(GPT, id=instance.id)  # Use instance.id to get the newly created object
            data = {
                'id': model.id,
                'slug': model.slug,
                'owner_id': model.owner.id if model.owner else None,
                'owner_slug': model.owner.slug if model.owner else None,
                'description': model.description,
                'generated_date': model.generatedDate,  # Change to 'generatedDate' to match model field name
                'tags': [tag.name for tag in model.tags.all()],
                'frameworks': model.frameworks,
                'upvotes': [{'date': point.date, 'count': point.count} for point in model.activitySummary.upvotes.all()],
                'views': [{'date': point.date, 'count': point.count} for point in model.activitySummary.views.all()],
                'featured': model.featured,
                'tryitout_link': model.tryitout_link
            }
            return JsonResponse(data, safe=False)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
