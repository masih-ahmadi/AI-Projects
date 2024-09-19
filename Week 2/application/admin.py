from django.contrib import admin
from .models import storyHistory
# Register your models here.

@admin.register(storyHistory)
class StoryHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'friend_name', 'story_topic', 'created_at')
    search_fields = ('name', 'friend_name', 'story_topic')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

