from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser , Course
#why do we need this form?
#  If we didn't use this form, you would have to:

# Write raw HTML <input> tags for every single field.

# Write custom Python logic to grab the data from the request.

# Write complex security logic to securely hash the user's password (never store raw passwords!).

# Write logic to check if the two password fields match.

# Manually save the data to the database.

class CustomSignupForm(UserCreationForm):
    # By inheriting from UserCreationForm, Django handles all the password hashing, validation,
    # and HTML generation for you. We just needed to create this
    # custom version because Django's default form didn't 
    # know your address field existed!
    
    email = forms.EmailField(
        required=True,
        help_text="A valid email address is required."
    )
    first_name = forms.CharField(
        max_length=150,
        required=True,
        help_text="First name is required."
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        help_text="Last name is required."
    )
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name", "address")
    
    def clean_email(self):
        """Validate email is unique and properly formatted"""
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email address is required.")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered.")
        if len(email) > 254:
            raise ValidationError("Email address is too long.")
        return email
    
    def clean_username(self):
        """Validate username"""
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("Username is required.")
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username
    
    def clean_first_name(self):
        """Validate first name"""
        first_name = self.cleaned_data.get('first_name')
        if not first_name or not first_name.strip():
            raise ValidationError("First name cannot be empty.")
        if len(first_name) < 2:
            raise ValidationError("First name must be at least 2 characters long.")
        if not first_name.replace(" ", "").isalpha():
            raise ValidationError("First name can only contain letters and spaces.")
        return first_name
    
    def clean_last_name(self):
        """Validate last name"""
        last_name = self.cleaned_data.get('last_name')
        if not last_name or not last_name.strip():
            raise ValidationError("Last name cannot be empty.")
        if len(last_name) < 2:
            raise ValidationError("Last name must be at least 2 characters long.")
        if not last_name.replace(" ", "").isalpha():
            raise ValidationError("Last name can only contain letters and spaces.")
        return last_name
    
    def clean_password2(self):
        """Validate password strength"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords do not match.")
            
            # Password strength requirements
            if len(password1) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            if not any(char.isupper() for char in password1):
                raise ValidationError("Password must contain at least one uppercase letter.")
            if not any(char.islower() for char in password1):
                raise ValidationError("Password must contain at least one lowercase letter.")
            if not any(char.isdigit() for char in password1):
                raise ValidationError("Password must contain at least one digit.")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
                raise ValidationError("Password must contain at least one special character (!@#$%^&*).")
        
        return password2
    
    def clean(self):
        """Overall form validation"""
        cleaned_data = super().clean()
        # Add any cross-field validations here if needed
        return cleaned_data

class CourseForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter course title',
        }),
        help_text="Course title must be between 3 and 100 characters."
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter course description',
            'rows': 6,
        }),
        help_text="Description must be at least 10 characters long."
    )
    
    class Meta:
        model = Course
        fields = ['title', 'description']
    
    def clean_title(self):
        """Validate title field"""
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise ValidationError("Course title cannot be empty.")
        if len(title) < 3:
            raise ValidationError("Course title must be at least 3 characters long.")
        if len(title) > 100:
            raise ValidationError("Course title cannot exceed 100 characters.")
        return title
    
    def clean_description(self):
        """Validate description field"""
        description = self.cleaned_data.get('description')
        if not description or not description.strip():
            raise ValidationError("Course description cannot be empty.")
        if len(description) < 10:
            raise ValidationError("Course description must be at least 10 characters long.")
        return description
    
    def clean(self):
        """Overall form validation"""
        cleaned_data = super().clean()
        return cleaned_data

class EmailAuthenticationForm(AuthenticationForm):
    """
    Custom login form that accepts email or username.
    """
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Email or Username',
        }),
        label="Email or Username",
        help_text="Enter your email address or username to log in."
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )
    
    def clean_username(self):
        """Validate username/email field"""
        username = self.cleaned_data.get('username')
        if not username or not username.strip():
            raise ValidationError("Email or username is required.")
        return username
    
    def clean(self):
        """Validate credentials"""
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = None
            try:
                # Try to get user by email
                user = CustomUser.objects.get(email=username)
            except CustomUser.DoesNotExist:
                try:
                    # Try to get user by username
                    user = CustomUser.objects.get(username=username)
                except CustomUser.DoesNotExist:
                    raise ValidationError(
                        "Invalid email/username or password. Please try again.",
                        code='invalid_login',
                    )
            
            # Check password
            if not user.check_password(password):
                raise ValidationError(
                    "Invalid email/username or password. Please try again.",
                    code='invalid_login',
                )
            
            if not user.is_active:
                raise ValidationError(
                    "This account is inactive.",
                    code='inactive',
                )
            
            self.user_cache = user
        
        return self.cleaned_data