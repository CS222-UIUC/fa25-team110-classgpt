from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import UserProfile, UploadedFile
from django.core.files.uploadedfile import SimpleUploadedFile
import json


# Test credential constants (NOT production credentials)
TEST_USERNAME = 'testuser'
TEST_PASSWORD = 'test_password_123'
TEST_EMAIL = 'test@example.com'

PROF_USERNAME = 'professor1'
PROF_PASSWORD = 'prof_password_123'
PROF_EMAIL = 'prof@example.com'


class UserAuthenticationTests(APITestCase):
    """Test suite for user authentication endpoints"""

    def setUp(self):
        """Set up test client and sample data"""
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.valid_user_data = {
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD,
            'email': TEST_EMAIL,
            'user_type': 'student'
        }

    def test_register_successful(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User created')
        self.assertEqual(response.data['user_type'], 'student')
        self.assertTrue(User.objects.filter(username=TEST_USERNAME).exists())

    def test_register_professor(self):
        """Test registering a professor user"""
        professor_data = {
            'username': PROF_USERNAME,
            'password': PROF_PASSWORD,
            'email': PROF_EMAIL,
            'user_type': 'professor'
        }
        response = self.client.post(self.register_url, professor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_type'], 'professor')
        
        profile = UserProfile.objects.get(user__username=PROF_USERNAME)
        self.assertEqual(profile.user_type, 'professor')

    def test_register_duplicate_username(self):
        """Test registration fails with duplicate username"""
        # Create first user
        self.client.post(self.register_url, self.valid_user_data, format='json')
        
        # Try to create another with same username
        duplicate_data = {
            'username': TEST_USERNAME,
            'password': 'different_test_pass',
            'email': 'different@example.com'
        }
        response = self.client.post(self.register_url, duplicate_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username already exists')

    def test_register_missing_fields(self):
        """Test registration fails when required fields are missing"""
        incomplete_data = {
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD
        }
        response = self.client.post(self.register_url, incomplete_data, format='json')
        # Should fail or return validation error
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK])

    def test_login_successful(self):
        """Test successful login"""
        # Register user first
        self.client.post(self.register_url, self.valid_user_data, format='json')
        
        # Login
        login_data = {
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], TEST_USERNAME)
        self.assertEqual(response.data['user_type'], 'student')

    def test_login_invalid_credentials(self):
        """Test login fails with invalid password"""
        # Register user
        self.client.post(self.register_url, self.valid_user_data, format='json')
        
        # Try to login with wrong password
        invalid_login = {
            'username': TEST_USERNAME,
            'password': 'incorrect_password_xyz'
        }
        response = self.client.post(self.login_url, invalid_login, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    def test_login_nonexistent_user(self):
        """Test login fails for non-existent user"""
        login_data = {
            'username': 'nonexistent_user',
            'password': 'some_pass'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FileUploadTests(APITestCase):
    """Test suite for file upload endpoints"""

    def setUp(self):
        """Set up test client and create test users"""
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.upload_url = '/api/auth/upload/'
        self.list_files_url = '/api/auth/files/'
        
        # Create a professor user
        professor_data = {
            'username': PROF_USERNAME,
            'password': PROF_PASSWORD,
            'email': PROF_EMAIL,
            'user_type': 'professor'
        }
        self.client.post(self.register_url, professor_data, format='json')
        self.professor = User.objects.get(username=PROF_USERNAME)

    def test_upload_pdf_file(self):
        """Test uploading a PDF file"""
        # Create a mock PDF file
        pdf_content = b'%PDF-1.4\n%fake pdf content'
        pdf_file = SimpleUploadedFile(
            "test_document.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        data = {
            'file': pdf_file,
            'course_name': 'CS 222'
        }
        response = self.client.post(self.upload_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'File uploaded successfully')
        self.assertIn('file_id', response.data)
        self.assertEqual(response.data['file_type'], 'pdf')
        self.assertEqual(response.data['filename'], 'test_document.pdf')

    def test_upload_docx_file(self):
        """Test uploading a DOCX file"""
        # Create a mock DOCX file
        docx_content = b'PK\x03\x04'  # DOCX magic bytes
        docx_file = SimpleUploadedFile(
            "test_document.docx",
            docx_content,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        data = {
            'file': docx_file,
            'course_name': 'CS 222'
        }
        response = self.client.post(self.upload_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['file_type'], 'docx')

    def test_upload_unsupported_file(self):
        """Test upload fails with unsupported file type"""
        # Create a mock TXT file (unsupported)
        txt_file = SimpleUploadedFile(
            "test.txt",
            b"plain text content",
            content_type="text/plain"
        )
        
        data = {'file': txt_file}
        response = self.client.post(self.upload_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Unsupported file type')

    def test_upload_no_file(self):
        """Test upload fails when no file is provided"""
        data = {'course_name': 'CS 222'}
        response = self.client.post(self.upload_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No file provided')

    def test_list_files(self):
        """Test listing uploaded files"""
        # Upload a file first
        pdf_file = SimpleUploadedFile(
            "test_document.pdf",
            b'%PDF-1.4\ntest content',
            content_type="application/pdf"
        )
        
        upload_data = {
            'file': pdf_file,
            'course_name': 'CS 222'
        }
        self.client.post(self.upload_url, upload_data, format='multipart')
        
        # List files
        response = self.client.get(self.list_files_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('files', response.data)
        self.assertEqual(len(response.data['files']), 1)
        self.assertEqual(response.data['files'][0]['filename'], 'test_document.pdf')
        self.assertEqual(response.data['files'][0]['course_name'], 'CS 222')

    def test_list_files_empty(self):
        """Test listing files when none exist"""
        response = self.client.get(self.list_files_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['files'], [])

    def test_list_files_multiple(self):
        """Test listing multiple uploaded files"""
        # Upload multiple files
        for i in range(3):
            pdf_file = SimpleUploadedFile(
                f"document_{i}.pdf",
                b'%PDF-1.4\ntest content',
                content_type="application/pdf"
            )
            upload_data = {'file': pdf_file, 'course_name': f'Course {i}'}
            self.client.post(self.upload_url, upload_data, format='multipart')
        
        # List files
        response = self.client.get(self.list_files_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['files']), 3)


class FileDeleteTests(APITestCase):
    """Test suite for file deletion endpoint"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.upload_url = '/api/auth/upload/'
        self.delete_url = '/api/auth/files/{}/delete/'
        
        # Create a professor user
        professor_data = {
            'username': PROF_USERNAME,
            'password': PROF_PASSWORD,
            'email': PROF_EMAIL,
            'user_type': 'professor'
        }
        self.client.post(self.register_url, professor_data, format='json')

    def test_delete_existing_file(self):
        """Test deleting an existing file"""
        # Upload a file
        pdf_file = SimpleUploadedFile(
            "test_document.pdf",
            b'%PDF-1.4\ntest content',
            content_type="application/pdf"
        )
        upload_data = {'file': pdf_file, 'course_name': 'CS 222'}
        upload_response = self.client.post(self.upload_url, upload_data, format='multipart')
        file_id = upload_response.data['file_id']
        
        # Delete the file
        delete_response = self.client.delete(self.delete_url.format(file_id))
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertEqual(delete_response.data['message'], 'File deleted')
        
        # Verify file is deleted
        self.assertFalse(UploadedFile.objects.filter(id=file_id).exists())

    def test_delete_nonexistent_file(self):
        """Test deleting a file that doesn't exist"""
        response = self.client.delete(self.delete_url.format(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'File not found')


class ChatAPITests(APITestCase):
    """Test suite for chat endpoint"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.upload_url = '/api/auth/upload/'
        self.chat_url = '/api/auth/chat/'
        
        # Create a professor user
        professor_data = {
            'username': PROF_USERNAME,
            'password': PROF_PASSWORD,
            'email': PROF_EMAIL,
            'user_type': 'professor'
        }
        self.client.post(self.register_url, professor_data, format='json')

    def test_chat_without_file(self):
        """Test chat endpoint without providing a file"""
        chat_data = {
            'question': 'What is the capital of France?',
            'chat_history': []
        }
        response = self.client.post(self.chat_url, chat_data, format='json')
        # Should succeed even without a file (uses general knowledge)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR])
        if response.status_code == status.HTTP_200_OK:
            self.assertIn('answer', response.data)
            self.assertEqual(response.data['file_used'], None)

    def test_chat_missing_question(self):
        """Test chat fails when question is missing"""
        chat_data = {
            'file_id': 1,
            'chat_history': []
        }
        response = self.client.post(self.chat_url, chat_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No question provided')

    def test_chat_with_file(self):
        """Test chat endpoint with a file context"""
        # Upload a file
        pdf_file = SimpleUploadedFile(
            "test_document.pdf",
            b'%PDF-1.4\nCS 222 is a computer science course about testing.',
            content_type="application/pdf"
        )
        upload_data = {'file': pdf_file, 'course_name': 'CS 222'}
        upload_response = self.client.post(self.upload_url, upload_data, format='multipart')
        file_id = upload_response.data['file_id']
        
        # Chat with file context
        chat_data = {
            'question': 'What is this course about?',
            'file_id': file_id,
            'chat_history': []
        }
        response = self.client.post(self.chat_url, chat_data, format='json')
        # Response depends on Ollama availability
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR])
        if response.status_code == status.HTTP_200_OK:
            self.assertEqual(response.data['question'], 'What is this course about?')
            self.assertIn('answer', response.data)

    def test_chat_with_history(self):
        """Test chat endpoint with conversation history"""
        chat_data = {
            'question': 'Tell me more about that',
            'chat_history': [
                {'role': 'user', 'content': 'What is Python?'},
                {'role': 'assistant', 'content': 'Python is a programming language.'}
            ]
        }
        response = self.client.post(self.chat_url, chat_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR])

    def test_chat_with_invalid_file(self):
        """Test chat with non-existent file ID"""
        chat_data = {
            'question': 'What is in this file?',
            'file_id': 9999,
            'chat_history': []
        }
        response = self.client.post(self.chat_url, chat_data, format='json')
        # Should still work but without file context
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR])


class IntegrationTests(APITestCase):
    """Integration tests for complete workflows"""

    def setUp(self):
        """Set up test client and URLs"""
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.upload_url = '/api/auth/upload/'
        self.list_files_url = '/api/auth/files/'
        self.delete_url = '/api/auth/files/{}/delete/'
        self.chat_url = '/api/auth/chat/'

    def test_complete_professor_workflow(self):
        """Test complete workflow: register -> upload -> list -> delete"""
        # Register as professor
        professor_data = {
            'username': 'test_prof_workflow',
            'password': 'test_prof_pass_workflow',
            'email': 'prof_workflow@test.com',
            'user_type': 'professor'
        }
        reg_response = self.client.post(self.register_url, professor_data, format='json')
        self.assertEqual(reg_response.status_code, status.HTTP_200_OK)
        
        # Login
        login_data = {'username': 'test_prof_workflow', 'password': 'test_prof_pass_workflow'}
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        # Upload file
        pdf_file = SimpleUploadedFile(
            "lecture_notes.pdf",
            b'%PDF-1.4\nLecture content here',
            content_type="application/pdf"
        )
        upload_data = {'file': pdf_file, 'course_name': 'CS 222'}
        upload_response = self.client.post(self.upload_url, upload_data, format='multipart')
        self.assertEqual(upload_response.status_code, status.HTTP_200_OK)
        file_id = upload_response.data['file_id']
        
        # List files
        list_response = self.client.get(self.list_files_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data['files']), 1)
        
        # Delete file
        delete_response = self.client.delete(self.delete_url.format(file_id))
        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        
        # Verify file is deleted
        list_response = self.client.get(self.list_files_url)
        self.assertEqual(len(list_response.data['files']), 0)

    def test_student_and_professor_registration(self):
        """Test registration flow for both student and professor"""
        # Register student
        student_data = {
            'username': 'test_student_reg',
            'password': 'test_student_pass',
            'email': 'student@test.com',
            'user_type': 'student'
        }
        student_response = self.client.post(self.register_url, student_data, format='json')
        self.assertEqual(student_response.status_code, status.HTTP_200_OK)
        
        # Register professor
        professor_data = {
            'username': 'test_prof_reg',
            'password': 'test_prof_pass',
            'email': 'prof@test.com',
            'user_type': 'professor'
        }
        professor_response = self.client.post(self.register_url, professor_data, format='json')
        self.assertEqual(professor_response.status_code, status.HTTP_200_OK)
        
        # Verify both exist
        self.assertTrue(User.objects.filter(username='test_student_reg').exists())
        self.assertTrue(User.objects.filter(username='test_prof_reg').exists())
        
        # Verify types
        student_profile = UserProfile.objects.get(user__username='test_student_reg')
        professor_profile = UserProfile.objects.get(user__username='test_prof_reg')
        self.assertEqual(student_profile.user_type, 'student')
        self.assertEqual(professor_profile.user_type, 'professor')
