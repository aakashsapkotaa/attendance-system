from django.contrib import admin
from .models import Department, Course

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head')
    search_fields = ('name', 'code')
    list_filter = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'teacher', 'start_date', 'end_date')
    list_filter = ('department', 'start_date', 'end_date')
    search_fields = ('name', 'code', 'description')
    filter_horizontal = ('students',)
    prepopulated_fields = {'slug': ('name',)}
