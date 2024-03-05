from django.db import models

class Owner(models.Model):
    id = models.IntegerField(primary_key=True)
    slug = models.CharField(max_length=255)

class ModelStats(models.Model):
    name = models.CharField(max_length=255)
    value = models.IntegerField()

class TimeSeriesPoint(models.Model):
    date = models.DateTimeField()
    count = models.IntegerField()

class Tags(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class Category(models.Model):
    tags = models.ManyToManyField(Tags)
    type = models.CharField(max_length=255)

class ActivitySummary(models.Model):
    id = models.IntegerField(primary_key=True)
    generatedDate = models.DateTimeField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)
    modelStats = models.ManyToManyField(ModelStats)
    downloads = models.ManyToManyField(TimeSeriesPoint, related_name='downloads')
    views = models.ManyToManyField(TimeSeriesPoint, related_name='views')
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE, null=True)

class GPT(models.Model):
    id = models.IntegerField(primary_key=True)
    slug = models.CharField(max_length=255)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    description = models.TextField()
    activitySummary = models.OneToOneField(ActivitySummary, on_delete=models.CASCADE)
    categories = models.OneToOneField(Category, on_delete=models.CASCADE)
    frameworks = models.CharField(max_length=255)  # Assuming only one framework for simplicity
