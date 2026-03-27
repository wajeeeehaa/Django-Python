from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomSignupForm , CourseForm, EmailAuthenticationForm
from .models import Student, Course

def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            student = Student(user=new_user)
            student.full_clean()  # Run model validation
            student.save()
            return redirect("login")
    else:
        form = CustomSignupForm()
    return render(request, "students/signup.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'students/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


@login_required(login_url='login')
def student_dashboard(request):
    # Get or create Student profile for the user
    current_student, created = Student.objects.get_or_create(user=request.user)
    enrolled_course = current_student.course
    context = {
        'student': current_student,
        'course': enrolled_course,
    }
    return render(request, "students/dashboard.html", context)

@login_required(login_url='login')
def course_catalog(request):
    # Fetches all courses from the database
    all_courses = Course.objects.all() 
    return render(request, "students/catalog.html", {"courses": all_courses})

@login_required(login_url='login')
def enroll_course(request, course_id):
    if request.method == "POST":
        selected_course = Course.objects.get(id=course_id)
        current_student, created = Student.objects.get_or_create(user=request.user)
        
        
        current_student.course = selected_course
        current_student.full_clean()  
        current_student.save() 
        
        return redirect("student_dashboard")
    return redirect("course_catalog")


def check_if_instructor(user):
    return user.is_staff

@user_passes_test(check_if_instructor, login_url='login')
def create_course_view(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.full_clean()  
            course.save()
            return redirect("course_catalog")
    else:
        form = CourseForm()
    return render(request, "students/create_course.html", {"form": form})