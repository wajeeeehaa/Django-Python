from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Student Pages
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('catalog/', views.course_catalog, name='course_catalog'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    
    # Instructor Page
    path('create-course/', views.create_course_view, name='create_course'),
]