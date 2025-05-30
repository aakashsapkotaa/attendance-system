from django.contrib import admin
from .models import Session, AttendanceRecord

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'date', 'start_time', 'end_time', 'is_active')
    list_filter = ('date', 'course', 'is_active')
    search_fields = ('course__name', 'course__code', 'description')
    date_hierarchy = 'date'

class AttendanceInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0
    fields = ('student', 'status', 'time_in', 'time_out', 'marked_with', 'marked_by')
    readonly_fields = ('marked_by',)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status', 'time_in', 'time_out', 'marked_with')
    list_filter = ('status', 'marked_with', 'session__date')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'session__course__name')
    date_hierarchy = 'session__date'
    
    def save_model(self, request, obj, form, change):
        if not obj.marked_by:
            obj.marked_by = request.user
        super().save_model(request, obj, form, change)
