from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomSignupForm , CourseForm, EmailAuthenticationForm, StudentCourseSelectionForm
from .models import CustomUser, Course

def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            new_user = form.save()
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
            # Redirect everyone to student dashboard (superusers can access admin from there)
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
    enrolled_courses = request.user.courses.all()
    context = {
        'courses': enrolled_courses,
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
        request.user.courses.add(selected_course)
        
        return redirect("student_dashboard")
    return redirect("course_catalog")


def check_if_instructor(user):
    return user.role == 'instructor' or user.is_staff

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

@user_passes_test(check_if_instructor, login_url='login')
def manage_courses_view(request):
    """Admin view to see all courses with edit/delete options"""
    all_courses = Course.objects.all()
    context = {
        'courses': all_courses,
    }
    return render(request, "students/manage_courses.html", context)

@user_passes_test(check_if_instructor, login_url='login')
def edit_course_view(request, course_id):
    """Admin view to edit a course"""
    course = Course.objects.get(id=course_id)
    
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            updated_course = form.save(commit=False)
            updated_course.full_clean()
            updated_course.save()
            return redirect("manage_courses")
    else:
        form = CourseForm(instance=course)
    
    return render(request, "students/edit_course.html", {"form": form, "course": course})

@user_passes_test(check_if_instructor, login_url='login')
def delete_course_view(request, course_id):
    """Admin view to delete a course"""
    course = Course.objects.get(id=course_id)
    
    if request.method == "POST":
        course.delete()
        return redirect("manage_courses")
    
    return render(request, "students/delete_course.html", {"course": course})


@login_required(login_url='login')
def select_multiple_courses(request):
    """View for students to select and enroll in multiple courses at once"""
    if request.method == "POST":
        form = StudentCourseSelectionForm(request.POST)
        if form.is_valid():
            selected_courses = form.cleaned_data['courses']
            # Add all selected courses to the user's enrollment
            for course in selected_courses:
                request.user.courses.add(course)
            return redirect('student_dashboard')
    else:
        form = StudentCourseSelectionForm()
    
    # Get courses already enrolled in
    enrolled_course_ids = request.user.courses.values_list('id', flat=True)
    # Filter out already enrolled courses from the form queryset
    form.fields['courses'].queryset = Course.objects.exclude(id__in=enrolled_course_ids)
    
    context = {'form': form}
    return render(request, 'students/select_courses.html', context)