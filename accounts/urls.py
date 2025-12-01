from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login_view),
    path('upload/', views.upload_file),
    path('files/', views.list_files),
    path('files/<int:file_id>/delete/', views.delete_file),
]
