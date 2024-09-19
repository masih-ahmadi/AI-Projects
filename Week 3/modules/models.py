from django.db import models
from django.utils import timezone
# Create your models here.
class Module(models.Model):
    module_name = models.CharField(max_length=255)
    professor = models.CharField(max_length=255)
    assessment = models.CharField(max_length=255)
    outcomes = models.CharField(max_length=255)
    credits = models.IntegerField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.module_name


