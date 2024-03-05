from rest_framework import serializers
from .models import GPT

class GPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPT
        fields = ['id', 'slug', 'owner', 'description', 'activity_summary', 'categories', 'frameworks']
