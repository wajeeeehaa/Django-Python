from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows login with email or username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to authenticate with email first
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # If email doesn't exist, try with username
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        
        # Check password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
