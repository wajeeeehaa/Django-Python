from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.decorators import login_required 
from .models import Student
from .forms import StudentForm
# Create your views here.

@login_required(login_url='/myapp/login')
def home(request):
    return render(request,"myapp/index.html")
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/myapp/login/")
        else:
            return render(request, "myapp/register.html", {"form": form})
    else:
        form = UserCreationForm()
        return render(request, "myapp/register.html", {"form": form})
def login_view(request):
    if request.method == "POST":
        form= AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            if user.is_authenticated:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "myapp/login.html",{"form":form})
def logout_view(request):
    logout(request)
    return redirect("home")
@login_required(login_url="myapp/login")
def student_list(request):
    students= Student.objects.all()
    return render(request,"myapp/studentlist.html",{"students":students})
@login_required(login_url="myapp/login")
def student_create(request):
    if request.method == "POST":
        form= StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form= StudentForm()
    return render(request,"myapp/student_form.html",{"form":form})

@login_required(login_url="myapp/login")
def student_update(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)
    return render(request, "myapp/student_form.html", {"form": form})

@login_required(login_url="myapp/login")
def student_delete(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == "POST":
        student.delete()
        return redirect("student_list")
    return render(request, "myapp/student_confirm_delete.html", {"student": student})