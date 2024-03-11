from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import GPT, Owner, ActivitySummary, Tags
from .serializers import GPTSerializer
from django.views.decorators.csrf import csrf_exempt
import datetime
import pytz
import json
from django.db import transaction
from django.db.models import Sum


@csrf_exempt
def get_models(request):
    models = GPT.objects.all().values('id', 'slug', 'description', 'featured','tryitout_link', 'owner__slug', 'total_upvote', 'total_view')
    for model in models:
        tags = Tags.objects.filter(gpt__id=model['id']).values_list('name', flat=True)
        model['tags'] = list(tags)
    return JsonResponse(list(models), safe=False)

@csrf_exempt
def get_model_details(request, id):
    model = get_object_or_404(GPT, id=id)
    
    # Refresh total_upvote and total_view fields
    upvotes_count = model.activity_summary.upvotes.aggregate(Sum('count'))['count__sum']
    views_count = model.activity_summary.views.aggregate(Sum('count'))['count__sum']
    model.total_upvote = upvotes_count if upvotes_count else 0
    model.total_view = views_count if views_count else 0
    model.save()

    context = {
        'id': model.id,
        'slug': model.slug,
        'owner_id': model.owner.id if model.owner else None,
        'owner_slug': model.owner.slug if model.owner else None,
        'description': model.description,
        'generated_date': model.generated_date,
        'tags': [tag.name for tag in model.tags.all()] if model.tags else None,
        'frameworks': model.frameworks,
        'upvotes': [{'date': point.date, 'count': point.count} for point in model.activity_summary.upvotes.all()],
        'views': [{'date': point.date, 'count': point.count} for point in model.activity_summary.views.all()],
        'total_upvote': model.total_upvote,
        'total_view': model.total_view,
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
    model.total_upvote += 1  
    model.save()  # Save the model
    return JsonResponse({'message': 'Upvote count updated successfully'})

@csrf_exempt
def update_view(request, id):
    model = get_object_or_404(GPT, id=id)
    current_date = datetime.datetime.now(pytz.utc).date()
    time_series_point, created = model.activity_summary.views.get_or_create(date=current_date, defaults={'count': 1})
    if not created:
        time_series_point.count += 1
        time_series_point.save()
    model.total_view += 1  # Update total_view field
    model.save()  # Save the model
    return JsonResponse({'message': 'View count updated successfully'})

@csrf_exempt
def add_gpt_model(request):
    if request.method == 'POST':
        # Decode the request body from bytes to string
        body = request.body.decode('utf-8')

        # Parse the string as JSON
        data = json.loads(body)

        # Using dictionary comprehension to filter out None values
        gpt_data = {
            'slug': data.get('slug', ''),
            'owner': data.get('owner_id'),
            'description': data.get('description', ''),
            'generated_date': data.get('generated_date'),  
            'tags': data.get('tags', []),
            'frameworks': data.get('frameworks'),
            'featured': data.get('featured', False),
            'tryitout_link': data.get('tryitout_link', ''),
        }

        # Using transaction.atomic() to ensure atomicity
        with transaction.atomic():
            # Create the GPT instance
            serializer = GPTSerializer(data=gpt_data)
            if serializer.is_valid():
                model = serializer.save()

                # Create ActivitySummary instance with one view and one upvote
                activity_summary = ActivitySummary.objects.create()
                activity_summary.views.create(date=model.generated_date, count=1)
                activity_summary.upvotes.create(date=model.generated_date, count=1)

                # Assign the activity_summary to the GPT model
                model.activity_summary = activity_summary
                model.save()

                # Generate response data
                data = {
                    'id': model.id,
                    'slug': model.slug,
                    'owner_id': model.owner.id if model.owner else None,
                    'owner_slug': model.owner.slug if model.owner else None,
                    'description': model.description,
                    'generated_date': model.generated_date,  
                    'tags': [tag.name for tag in model.tags.all()] if model.tags else None,
                    'frameworks': model.frameworks,
                    'total_upvote': model.total_upvote,
                    'total_view': model.total_view,
                    'featured': model.featured,
                    'tryitout_link': model.tryitout_link
                } 

                # Return JsonResponse with the response data
                return JsonResponse(data, safe=False)

            # Return JsonResponse with serializer errors if GPT creation fails
            return JsonResponse({'errors': [serializer.errors]}, status=400)

@csrf_exempt
def get_all_tags(request):
    tags = Tags.objects.all().values_list('name', flat=True)
    return JsonResponse({'tags': list(tags)})

@csrf_exempt
def get_all_owners(request):
    owners = Owner.objects.all().values_list('slug', flat=True)
    return JsonResponse({'owners': list(owners)})


