from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        from django.contrib.auth.models import User
        from accounts.models import UserProfile

        username = "testuser"
        password = "12345"

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password, email="test@example.com")
            UserProfile.objects.create(user=user, user_type="student")
            print(f"✅ Created default test user: {username} / {password}")