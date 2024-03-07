from django.db import models

class Owner(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=255)

class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    
class TimeSeriesPoint(models.Model):
    date = models.DateTimeField()
    count = models.IntegerField()
    
class ActivitySummary(models.Model):
    id = models.AutoField(primary_key=True)
    upvotes = models.ManyToManyField(TimeSeriesPoint, related_name='upvotes')
    views = models.ManyToManyField(TimeSeriesPoint, related_name='views')

class GPT(models.Model):
    id = models.AutoField(primary_key=True)
    slug = models.CharField(max_length=255)  # Unique identifier for GPT instance
    generated_date = models.DateTimeField()  # Date when the GPT instance was generated
    description = models.TextField()  # Description of the GPT instance
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)  # Owner of the GPT instance
    tags = models.ManyToManyField(Tags, blank=True)  # Tags associated with the GPT instance
    frameworks = models.CharField(max_length=255)  # Assuming only one framework for simplicity
    featured = models.BooleanField(default=False)  # Whether the GPT instance is featured or not
    tryitout_link = models.CharField(max_length=255, default="")  # Link for trying out the GPT instance
    activity_summary = models.ForeignKey(ActivitySummary, on_delete=models.CASCADE, null=True, default=None)  # Relationship with ActivitySummary
