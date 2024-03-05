from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import GPT, ActivitySummary

def get_models(request):
    models = GPT.objects.all().values('id', 'slug', 'downloads', 'views')
    return JsonResponse(list(models), safe=False)

def get_model_details(request, id):
    model = get_object_or_404(GPT, id=id)
    return JsonResponse(model.to_dict(), safe=False)

def update_download(request, id):
    model = get_object_or_404(GPT, id=id)
    model.downloads += 1
    model.save()
    return JsonResponse({'message': 'Download count updated successfully'})

def update_upvote(request, id):
    model = get_object_or_404(GPT, id=id)
    model.upvotes += 1
    model.save()
    return JsonResponse({'message': 'Upvote count updated successfully'})

def update_view(request, id):
    model = get_object_or_404(GPT, id=id)
    model.views += 1
    model.save()
    return JsonResponse({'message': 'View count updated successfully'})
