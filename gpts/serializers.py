from rest_framework import serializers
from .models import GPT, ActivitySummary

class ActivitySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitySummary
        fields = '__all__'

class GPTSerializer(serializers.ModelSerializer):
    activitySummary = ActivitySummarySerializer() 

    class Meta:
        model = GPT
        fields = '__all__'

