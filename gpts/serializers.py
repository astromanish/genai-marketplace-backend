from rest_framework import serializers
from .models import GPT

class GPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPT
        fields = ['id', 'slug', 'upvote', 'download', 'view_count', 'owner', 'description', 'activity_summary', 'model_stats', 'time_series', 'downloads', 'title', 'points', 'views', 'categories', 'tags', 'dataset_count', 'competition_count', 'notebook_count', 'display_name', 'model_count', 'type', 'frameworks']
