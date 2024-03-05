from django.db import models

class ActivitySummary(models.Model):
    id = models.IntegerField(primary_key=True)
    generated_date = models.DateTimeField()

class ModelStat(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField()

class Point(models.Model):
    date = models.DateTimeField()
    count = models.IntegerField()

class Tag(models.Model):
    name = models.CharField(max_length=255)

class Category(models.Model):
    name = models.CharField(max_length=255)
    full_path = models.CharField(max_length=255)
    listing_url = models.CharField(max_length=255)

class GPT(models.Model):
    slug = models.CharField(max_length=255)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField()
    activity_summary = models.OneToOneField(ActivitySummary, on_delete=models.CASCADE)
    model_stats = models.ManyToManyField(ModelStat)
    time_series = models.JSONField()
    downloads = models.JSONField()
    title = models.CharField(max_length=255)
    points = models.ManyToManyField(Point)
    views = models.JSONField()
    categories = models.JSONField()
    tags = models.ManyToManyField(Tag)
    dataset_count = models.IntegerField()
    competition_count = models.IntegerField()
    notebook_count = models.IntegerField()
    display_name = models.CharField(max_length=255)
    model_count = models.IntegerField()
    type = models.CharField(max_length=255)
    frameworks = models.JSONField()
