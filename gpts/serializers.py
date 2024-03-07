from rest_framework import serializers
from .models import GPT

class GPTSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPT
        fields = '__all__'

