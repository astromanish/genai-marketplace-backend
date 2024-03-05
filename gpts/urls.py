from django.urls import path
from . import views

urlpatterns = [
    path('model', views.get_models, name='get_models'),
    path('model/<int:id>', views.get_model_details, name='get_model_details'),
    path('model/<int:id>/download', views.update_download, name='update_download'),
    path('model/<int:id>/upvote', views.update_upvote, name='update_upvote'),
    path('model/<int:id>/view', views.update_view, name='update_view'),
]
