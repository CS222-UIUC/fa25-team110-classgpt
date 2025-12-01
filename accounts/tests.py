from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import UserProfile


class LoginTest(TestCase):
	"""Tests for login behavior.

	- test_client_login: uses Django test client to log in (session auth)
	- test_login_view_post: posts JSON to the project's login endpoint
	  (/api/auth/login/) which is implemented with DRF's @api_view.
	"""

	def setUp(self):
		User = get_user_model()
		self.username = "testuser"
		self.password = "testpass"
		# Create the user and associated UserProfile (the login view expects a profile)
		self.user = User.objects.create_user(username=self.username, email="test@example.com", password=self.password)
		UserProfile.objects.create(user=self.user, user_type="student")

	def test_client_login(self):
		"""Verify Django's test client can log in the created user."""
		logged_in = self.client.login(username=self.username, password=self.password)
		self.assertTrue(logged_in)

	def test_login_view_post(self):
		"""POST to the DRF login view and assert a successful response and payload."""
		api_client = APIClient()
		response = api_client.post('/api/auth/login/', {'username': self.username, 'password': self.password}, format='json')
		self.assertEqual(response.status_code, 200)
		self.assertIn('username', response.data)
		self.assertIn('user_type', response.data)
		self.assertEqual(response.data['username'], self.username)

