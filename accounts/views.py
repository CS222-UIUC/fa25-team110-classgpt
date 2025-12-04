from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserProfile
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import extract_text, get_file_type
from .models import UploadedFile
import ollama

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
    
    # TEMPORARY: Get first professor user for testing
    # TODO: Use proper authentication later
    user = User.objects.filter(userprofile__user_type='professor').first()
    if not user:
        return Response({"error": "No professor user found"}, status=500)
    
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
    # TEMPORARY: Get first professor user
    user = User.objects.filter(userprofile__user_type='professor').first()
    if not user:
        return Response({"files": []})
    
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
        file = UploadedFile.objects.get(id=file_id)
        file.file.delete()
        file.delete()
        return Response({"message": "File deleted"})
    except UploadedFile.DoesNotExist:
        return Response({"error": "File not found"}, status=404)

@api_view(["POST"])
def chat(request):
    """Chat with AI about uploaded course materials"""
    question = request.data.get("question")
    file_id = request.data.get("file_id")
    chat_history = request.data.get("chat_history", [])  # Get chat history
    
    if not question:
        return Response({"error": "No question provided"}, status=400)
    
    # Get file content if file_id provided
    context = ""
    if file_id:
        try:
            file = UploadedFile.objects.get(id=file_id)
            context = f"Context from {file.original_filename}:\n{file.extracted_text}\n\n"
        except UploadedFile.DoesNotExist:
            pass
    
    # Build messages with history
    messages = []
    
    # Add system message with context
    if context:
        messages.append({
            'role': 'system',
            'content': f"{context}You are a helpful study assistant. Answer questions based on the course materials concisely."
        })
    
    # Add chat history
    for msg in chat_history:
        messages.append({
            'role': msg['role'],
            'content': msg['content']
        })
    
    # Add current question
    messages.append({
        'role': 'user',
        'content': question
    })
    
    try:
        # Call Ollama with full conversation
        response = ollama.chat(
            model='llama3.2:3b',
            messages=messages
        )
        
        answer = response['message']['content']
        
        return Response({
            "question": question,
            "answer": answer,
            "file_used": file.original_filename if file_id else None
        })
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)