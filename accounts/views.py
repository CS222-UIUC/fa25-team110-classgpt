from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserProfile
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import extract_text, get_file_type
from .models import UploadedFile


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    user_type = request.data.get("user_type", "student")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    UserProfile.objects.create(user=user, user_type=user_type)

    return Response({"message": "User created", "user_type": user_type})

@api_view(["POST"])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        profile = UserProfile.objects.get(user=user)
        return Response({"username": user.username, "user_type": profile.user_type})
    return Response({"error": "Invalid credentials"}, status=401)

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    if 'file' not in request.FILES:
        return Response({"error": "No file provided"}, status=400)
    
    file = request.FILES['file']
    course_name = request.data.get('course_name', '')
    
    user = request.user if request.user.is_authenticated else None
    if not user:
        return Response({"error": "Must be logged in"}, status=401)
    
    file_type = get_file_type(file.name)
    if not file_type:
        return Response({"error": "Unsupported file type"}, status=400)
    
    uploaded_file = UploadedFile.objects.create(
        professor=user,
        file=file,
        original_filename=file.name,
        file_type=file_type,
        course_name=course_name
    )
    
    file_path = uploaded_file.file.path
    extracted_text = extract_text(file_path, file_type)
    uploaded_file.extracted_text = extracted_text
    uploaded_file.save()
    
    return Response({
        "message": "File uploaded successfully",
        "file_id": uploaded_file.id,
        "filename": uploaded_file.original_filename,
        "file_type": uploaded_file.file_type
    })

@api_view(["GET"])
def list_files(request):
    user = request.user if request.user.is_authenticated else None
    if not user:
        return Response({"error": "Must be logged in"}, status=401)
    
    files = UploadedFile.objects.filter(professor=user).order_by('-uploaded_at')
    
    return Response({
        "files": [{
            "id": f.id,
            "filename": f.original_filename,
            "file_type": f.file_type,
            "course_name": f.course_name,
            "uploaded_at": f.uploaded_at,
        } for f in files]
    })

@api_view(["DELETE"])
def delete_file(request, file_id):
    try:
        file = UploadedFile.objects.get(id=file_id, professor=request.user)
        file.file.delete()
        file.delete()
        return Response({"message": "File deleted"})
    except UploadedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=404)