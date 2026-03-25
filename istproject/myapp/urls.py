from . import views
from django.urls import path
urlpatterns=[
    path("",views.home, name="home"),
    path("register/",views.register_view, name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),

    
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/update/<int:pk>/', views.student_update, name='student_update'),
    path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),


]