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
    
    # Instructor Pages
    path('create-course/', views.create_course_view, name='create_course'),
    path('manage-courses/', views.manage_courses_view, name='manage_courses'),
    path('edit-course/<int:course_id>/', views.edit_course_view, name='edit_course'),
    path('delete-course/<int:course_id>/', views.delete_course_view, name='delete_course'),
]