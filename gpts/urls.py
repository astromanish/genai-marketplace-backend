from django.urls import path
from . import views

urlpatterns = [
    path('model', views.get_models, name='get_models'),
    path('model/<int:id>', views.get_model_details, name='get_model_details'),
    path('model/<int:id>/upvote', views.update_upvote, name='update_upvote'),
    path('model/<int:id>/view', views.update_view, name='update_view'),
    path('model/add', views.add_gpt_model, name='add_gpt_model'),  # New API endpoint to add a new GPT model
    path('tags', views.get_all_tags, name='get_all_tags'),  # New API endpoint to get all available tags
]
