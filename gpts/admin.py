from django.contrib import admin
from .models import GPT, Tags, Owner

admin.site.register(GPT)
admin.site.register(Tags)
admin.site.register(Owner)