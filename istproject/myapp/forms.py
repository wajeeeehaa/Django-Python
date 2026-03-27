from django import forms
from django.core.exceptions import ValidationError
from .models import Student

class StudentForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter student name',
        }),
        help_text="Name must be at least 2 characters long."
    )
    age = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter age',
            'min': '5',
            'max': '100',
        }),
        help_text="Age must be between 5 and 100."
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address',
        }),
        help_text="Enter a valid email address."
    )
    grade = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter grade (e.g., A, B, C)',
        }),
        help_text="Enter student grade."
    )
    
    class Meta:
        model = Student
        fields = ["name", "age", "email", "grade"]
    
    def clean_name(self):
        """Validate name field"""
        name = self.cleaned_data.get('name')
        if not name or not name.strip():
            raise ValidationError("Student name cannot be empty.")
        if len(name) < 2:
            raise ValidationError("Student name must be at least 2 characters long.")
        if len(name) > 100:
            raise ValidationError("Student name cannot exceed 100 characters.")
        return name
    
    def clean_age(self):
        """Validate age field"""
        age = self.cleaned_data.get('age')
        if age is None:
            raise ValidationError("Age is required.")
        if age < 5:
            raise ValidationError("Student must be at least 5 years old.")
        if age > 100:
            raise ValidationError("Please enter a valid age (maximum 100).")
        return age
    
    def clean_email(self):
        """Validate email field"""
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Email address is required.")
        # Check if email already exists (for new records or if email changed)
        if self.instance.pk:  # Existing student
            if Student.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A student with this email already exists.")
        else:  # New student
            if Student.objects.filter(email=email).exists():
                raise ValidationError("A student with this email already exists.")
        return email
    
    def clean_grade(self):
        """Validate grade field"""
        grade = self.cleaned_data.get('grade')
        if not grade or not grade.strip():
            raise ValidationError("Grade cannot be empty.")
        valid_grades = ['A', 'B', 'C', 'D', 'E', 'F', 'A+', 'A-', 'B+', 'B-', 'C+', 'C-']
        if grade.upper() not in valid_grades:
            raise ValidationError(f"Grade must be one of: {', '.join(valid_grades)}")
        return grade
    
    def clean(self):
        """Overall form validation"""
        cleaned_data = super().clean()
        # Add any cross-field validations here if needed
        return cleaned_data