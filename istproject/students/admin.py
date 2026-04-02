# admin.py
from django.contrib import admin
from .models import CustomUser, Course

# Register CustomUser normally
admin.site.register(CustomUser)

# Customize the Course Admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    
    list_display = ('title', 'description') 
    search_fields = ('title',)

 