from django.db import models
from users.models import CustomUser
from core.models import Course
from django.utils import timezone

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.course.code} - {self.date} ({self.start_time} to {self.end_time})"
    
    class Meta:
        ordering = ['-date', 'start_time']
        unique_together = ['course', 'date', 'start_time']

class AttendanceRecord(models.Model):
    class AttendanceStatus(models.TextChoices):
        PRESENT = 'PRESENT', 'Present'
        ABSENT = 'ABSENT', 'Absent'
        LATE = 'LATE', 'Late'
        EXCUSED = 'EXCUSED', 'Excused'
    
    student = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        limit_choices_to={'role': CustomUser.Role.STUDENT}
    )
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.ABSENT
    )
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)
    marked_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='attendance_marked',
        limit_choices_to={'role__in': [CustomUser.Role.TEACHER, CustomUser.Role.ADMIN]}
    )
    marked_with = models.CharField(
        max_length=20,
        choices=[
            ('MANUAL', 'Manual Entry'),
            ('BARCODE', 'Barcode Scan'),
            ('FACE', 'Face Recognition'),
        ],
        default='MANUAL'
    )
    comments = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.session} - {self.status}"
    
    class Meta:
        unique_together = ['student', 'session']
        ordering = ['session', 'student']
