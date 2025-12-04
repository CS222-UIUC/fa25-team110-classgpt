from django.contrib import admin
from .models import UserProfile, UploadedFile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type']
    list_filter = ['user_type']
    search_fields = ['user__username', 'user__email']

@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'professor', 'file_type', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']