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
        'generated_date': model.generated_date,
        'tags': [model.tags.name] if model.tags else None,
        'frameworks': model.frameworks,
        'upvotes': [{'date': point.date, 'count': point.count} for point in model.activity_summary.upvotes.all()],
        'views': [{'date': point.date, 'count': point.count} for point in model.activity_summary.views.all()],
        'featured': model.featured,
        'tryitout_link': model.tryitout_link
    }
    return JsonResponse(context, safe=False)

@csrf_exempt
def update_upvote(request, id):
    model = get_object_or_404(GPT, id=id)
    current_date = datetime.datetime.now(pytz.utc).date()
    time_series_point, created = model.activity_summary.upvotes.get_or_create(date=current_date, defaults={'count': 1})
    if not created:
        time_series_point.count += 1
        time_series_point.save()
    return JsonResponse({'message': 'Upvote count updated successfully'})

@csrf_exempt
def update_view(request, id):
    model = get_object_or_404(GPT, id=id)
    current_date = datetime.datetime.now(pytz.utc).date()
    time_series_point, created = model.activity_summary.views.get_or_create(date=current_date, defaults={'count': 1})
    if not created:
        time_series_point.count += 1
        time_series_point.save()
    return JsonResponse({'message': 'View count updated successfully'})

@csrf_exempt
def add_gpt_model(request):
    current_date = datetime.datetime.now(pytz.utc).date()
    if request.method == 'POST':
        
        data = request.POST.copy()

        activitySummary = ActivitySummary.objects.create()
        activitySummary.views.create(date=current_date, count=1)
        activitySummary.upvotes.create(date=current_date, count=1)

        owner_id = data.get('owner_id')
        owner = Owner.objects.get(id=owner_id) if owner_id else None

        tag_ids = data.getlist('tag_ids')
        tags = Tags.objects.filter(id__in=tag_ids)

        gpt_data = {
            'slug': data.get('slug', ''),
            'owner': owner,  
            'description': data.get('description', ''),
            'generated_date': current_date,  # Change to 'generated_date' to match model field name
            'activitySummary': activitySummary,
            'tags': tags,  
            'frameworks': data.get('frameworks'),
            'featured': data.get('featured', False),
            'tryitout_link': data.get('tryitout_link', ''),
        }
        
        serializer = GPTSerializer(data=gpt_data)
        
        if serializer.is_valid():
            instance = serializer.save()
            model = get_object_or_404(GPT, id=instance.id)  
            data = {
                'id': model.id,
                'slug': model.slug,
                'owner_id': model.owner.id if model.owner else None,
                'owner_slug': model.owner.slug if model.owner else None,
                'description': model.description,
                'generated_date': model.generated_date,  
                'tags': [model.tags.name] if model.tags else None,
                'frameworks': model.frameworks,
                'upvotes': [{'date': point.date, 'count': point.count} for point in model.activity_summary.upvotes.all()],
                'views': [{'date': point.date, 'count': point.count} for point in model.activity_summary.views.all()],
                'featured': model.featured,
                'tryitout_link': model.tryitout_link
            }
            return JsonResponse(data, safe=False)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
