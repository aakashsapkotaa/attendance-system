from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Department, Course
from users.models import CustomUser
from attendance.models import Session, AttendanceRecord
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from users.views import is_admin, is_teacher_or_admin
import json

def landing_page(request):
    """Main landing page before login with options for admin or user login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing_page.html')

@login_required
def home(request):
    """Main landing page after login."""
    
    if request.user.is_student:
        # For students, show their courses and recent attendance
        courses = request.user.enrolled_courses.all()
        recent_sessions = Session.objects.filter(
            course__in=courses,
            date__gte=timezone.now().date() - timedelta(days=30)
        ).order_by('-date')[:5]
        
        attendance_records = AttendanceRecord.objects.filter(
            student=request.user,
            session__in=recent_sessions
        )
        
        # Get attendance statistics for the student
        total_sessions = AttendanceRecord.objects.filter(student=request.user).count()
        present_sessions = AttendanceRecord.objects.filter(
            student=request.user, 
            status=AttendanceRecord.AttendanceStatus.PRESENT
        ).count()
        
        attendance_rate = (present_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        context = {
            'courses': courses,
            'recent_sessions': recent_sessions,
            'attendance_records': attendance_records,
            'attendance_rate': attendance_rate,
            'total_sessions': total_sessions,
            'present_sessions': present_sessions
        }
        
        return render(request, 'core/student_dashboard.html', context)
    
    elif request.user.is_teacher:
        # For teachers, show courses they teach and upcoming sessions
        courses = Course.objects.filter(teacher=request.user)
        upcoming_sessions = Session.objects.filter(
            course__in=courses,
            date__gte=timezone.now().date()
        ).order_by('date', 'start_time')[:5]
        
        # Get attendance statistics for teacher's courses
        course_stats = []
        for course in courses:
            sessions = Session.objects.filter(course=course).count()
            students = course.students.count()
            attendance_rate = AttendanceRecord.objects.filter(
                session__course=course,
                status=AttendanceRecord.AttendanceStatus.PRESENT
            ).count() / (sessions * students) * 100 if sessions * students > 0 else 0
            
            course_stats.append({
                'course': course,
                'sessions': sessions,
                'students': students,
                'attendance_rate': attendance_rate
            })
        
        context = {
            'courses': courses,
            'upcoming_sessions': upcoming_sessions,
            'course_stats': course_stats
        }
        
        return render(request, 'core/teacher_dashboard.html', context)
    
    elif request.user.is_admin:
        # For admins, show system-wide statistics
        total_students = CustomUser.objects.filter(role=CustomUser.Role.STUDENT).count()
        total_teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER).count()
        total_courses = Course.objects.count()
        total_departments = Department.objects.count()
        total_sessions = Session.objects.count()
        
        # Get attendance statistics for all courses
        attendance_stats = {
            'total': AttendanceRecord.objects.count(),
            'present': AttendanceRecord.objects.filter(status=AttendanceRecord.AttendanceStatus.PRESENT).count(),
            'absent': AttendanceRecord.objects.filter(status=AttendanceRecord.AttendanceStatus.ABSENT).count(),
            'late': AttendanceRecord.objects.filter(status=AttendanceRecord.AttendanceStatus.LATE).count(),
            'excused': AttendanceRecord.objects.filter(status=AttendanceRecord.AttendanceStatus.EXCUSED).count(),
        }
        
        # Get attendance rate over time (last 7 days)
        attendance_trend = []
        for i in range(7, 0, -1):
            date = timezone.now().date() - timedelta(days=i)
            total = AttendanceRecord.objects.filter(session__date=date).count()
            present = AttendanceRecord.objects.filter(
                session__date=date,
                status=AttendanceRecord.AttendanceStatus.PRESENT
            ).count()
            
            rate = (present / total * 100) if total > 0 else 0
            attendance_trend.append({
                'date': date.strftime('%Y-%m-%d'),
                'rate': rate
            })
        
        context = {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'total_departments': total_departments,
            'total_sessions': total_sessions,
            'attendance_stats': attendance_stats,
            'attendance_trend': json.dumps(attendance_trend)
        }
        
        return render(request, 'core/admin_dashboard.html', context)
    
    # Fallback for any other role
    return render(request, 'core/dashboard.html')

# Department Views
@login_required
@user_passes_test(is_admin)
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'core/department_list.html', {'departments': departments})

@login_required
@user_passes_test(is_admin)
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    courses = Course.objects.filter(department=department)
    teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER, courses_taught__department=department).distinct()
    
    context = {
        'department': department,
        'courses': courses,
        'teachers': teachers
    }
    
    return render(request, 'core/department_detail.html', context)

@login_required
@user_passes_test(is_admin)
def department_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')
        head_id = request.POST.get('head')
        
        try:
            head = None
            if head_id:
                head = CustomUser.objects.get(id=head_id, role=CustomUser.Role.TEACHER)
            
            department = Department.objects.create(
                name=name,
                code=code,
                description=description,
                head=head
            )
            
            messages.success(request, f'Department "{department.name}" created successfully!')
            return redirect('department_detail', pk=department.pk)
            
        except Exception as e:
            messages.error(request, f'Error creating department: {str(e)}')
    
    # Get all teachers for the form
    teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER)
    return render(request, 'core/department_form.html', {'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')
        head_id = request.POST.get('head')
        
        try:
            head = None
            if head_id:
                head = CustomUser.objects.get(id=head_id, role=CustomUser.Role.TEACHER)
            
            department.name = name
            department.code = code
            department.description = description
            department.head = head
            department.save()
            
            messages.success(request, f'Department "{department.name}" updated successfully!')
            return redirect('department_detail', pk=department.pk)
            
        except Exception as e:
            messages.error(request, f'Error updating department: {str(e)}')
    
    # Get all teachers for the form
    teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER)
    return render(request, 'core/department_form.html', {'department': department, 'teachers': teachers})

@login_required
@user_passes_test(is_admin)
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        name = department.name
        department.delete()
        messages.success(request, f'Department "{name}" deleted successfully!')
        return redirect('department_list')
    
    return render(request, 'core/department_confirm_delete.html', {'department': department})

# Course Views
@login_required
def course_list(request):
    if request.user.is_admin:
        courses = Course.objects.all()
    elif request.user.is_teacher:
        courses = Course.objects.filter(teacher=request.user)
    else:  # Student
        courses = request.user.enrolled_courses.all()
    
    return render(request, 'core/course_list.html', {'courses': courses})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    # Check if user has permission to view this course
    if not request.user.is_admin and not request.user.is_teacher and course not in request.user.enrolled_courses.all():
        messages.error(request, "You don't have permission to view this course.")
        return redirect('course_list')
    
    sessions = Session.objects.filter(course=course).order_by('-date')
    students = course.students.all()
    
    # Calculate attendance statistics for this course
    attendance_stats = {}
    for student in students:
        records = AttendanceRecord.objects.filter(student=student, session__course=course)
        
        total = records.count()
        present = records.filter(status=AttendanceRecord.AttendanceStatus.PRESENT).count()
        absent = records.filter(status=AttendanceRecord.AttendanceStatus.ABSENT).count()
        late = records.filter(status=AttendanceRecord.AttendanceStatus.LATE).count()
        excused = records.filter(status=AttendanceRecord.AttendanceStatus.EXCUSED).count()
        
        attendance_rate = (present / total * 100) if total > 0 else 0
        
        attendance_stats[student.id] = {
            'total': total,
            'present': present,
            'absent': absent,
            'late': late,
            'excused': excused,
            'attendance_rate': attendance_rate
        }
    
    context = {
        'course': course,
        'sessions': sessions,
        'students': students,
        'attendance_stats': attendance_stats
    }
    
    return render(request, 'core/course_detail.html', context)

@login_required
@user_passes_test(is_teacher_or_admin)
def course_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')
        department_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        try:
            department = Department.objects.get(id=department_id)
            
            teacher = None
            if teacher_id:
                teacher = CustomUser.objects.get(id=teacher_id, role=CustomUser.Role.TEACHER)
            elif not request.user.is_admin:
                teacher = request.user  # Set current teacher if not admin
            
            course = Course.objects.create(
                name=name,
                code=code,
                description=description,
                department=department,
                teacher=teacher,
                start_date=start_date,
                end_date=end_date
            )
            
            # Add selected students
            student_ids = request.POST.getlist('students')
            if student_ids:
                students = CustomUser.objects.filter(id__in=student_ids, role=CustomUser.Role.STUDENT)
                course.students.set(students)
            
            messages.success(request, f'Course "{course.name}" created successfully!')
            return redirect('course_detail', pk=course.pk)
            
        except Exception as e:
            messages.error(request, f'Error creating course: {str(e)}')
    
    # Get data for the form
    departments = Department.objects.all()
    
    if request.user.is_admin:
        teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER)
    else:
        teachers = [request.user]  # Only current teacher if not admin
    
    students = CustomUser.objects.filter(role=CustomUser.Role.STUDENT)
    
    context = {
        'departments': departments,
        'teachers': teachers,
        'students': students
    }
    
    return render(request, 'core/course_form.html', context)

@login_required
@user_passes_test(is_teacher_or_admin)
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    # Check if user has permission to update this course
    if not request.user.is_admin and course.teacher != request.user:
        messages.error(request, "You don't have permission to update this course.")
        return redirect('course_list')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description')
        department_id = request.POST.get('department')
        teacher_id = request.POST.get('teacher')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        try:
            department = Department.objects.get(id=department_id)
            
            # Only admins can change the teacher
            if request.user.is_admin and teacher_id:
                teacher = CustomUser.objects.get(id=teacher_id, role=CustomUser.Role.TEACHER)
                course.teacher = teacher
            
            course.name = name
            course.code = code
            course.description = description
            course.department = department
            course.start_date = start_date
            course.end_date = end_date
            course.save()
            
            # Update students
            student_ids = request.POST.getlist('students')
            if student_ids:
                students = CustomUser.objects.filter(id__in=student_ids, role=CustomUser.Role.STUDENT)
                course.students.set(students)
            else:
                course.students.clear()
            
            messages.success(request, f'Course "{course.name}" updated successfully!')
            return redirect('course_detail', pk=course.pk)
            
        except Exception as e:
            messages.error(request, f'Error updating course: {str(e)}')
    
    # Get data for the form
    departments = Department.objects.all()
    
    if request.user.is_admin:
        teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER)
    else:
        teachers = [request.user]  # Only current teacher if not admin
    
    students = CustomUser.objects.filter(role=CustomUser.Role.STUDENT)
    selected_students = course.students.all()
    
    context = {
        'course': course,
        'departments': departments,
        'teachers': teachers,
        'students': students,
        'selected_students': selected_students
    }
    
    return render(request, 'core/course_form.html', context)

@login_required
@user_passes_test(is_teacher_or_admin)
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    # Check if user has permission to delete this course
    if not request.user.is_admin and course.teacher != request.user:
        messages.error(request, "You don't have permission to delete this course.")
        return redirect('course_list')
    
    if request.method == 'POST':
        name = course.name
        course.delete()
        messages.success(request, f'Course "{name}" deleted successfully!')
        return redirect('course_list')
    
    return render(request, 'core/course_confirm_delete.html', {'course': course})
