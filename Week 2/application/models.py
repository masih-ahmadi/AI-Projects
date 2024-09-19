from django.db import models
from django.conf import settings


# Create your models here.

class storyHistory(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field='id'
    )
    name = models.CharField(max_length=100)
    friend_name = models.CharField(max_length=100)
    story_topic = models.CharField(max_length=100)
    generated_story = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Story" 
        verbose_name_plural = "Stories" 

class user_log(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field='id'
    )
    story = models.TextField
    
