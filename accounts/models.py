from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ("student", "Student"),
        ("professor", "Professor"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="student")

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class UploadedFile(models.Model):
    FILE_TYPE_CHOICES = (
        ("pdf", "PDF"),
        ("docx", "Word Document"),
    )
    
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_files")
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    original_filename = models.CharField(max_length=255)
    extracted_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    course_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.original_filename} by {self.professor.username}"