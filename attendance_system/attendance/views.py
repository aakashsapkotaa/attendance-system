from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Session, AttendanceRecord
from .forms import SessionForm, AttendanceRecordForm, BulkAttendanceForm, BarcodeAttendanceForm
from users.models import CustomUser
from core.models import Course
from users.views import is_admin, is_teacher_or_admin
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
import json
import datetime
import csv
import io
import xlsxwriter
from .face_recognition import face_recognition_system
from django.db import models

def attendance_home(request):
    """
    Home page for the attendance section.
    """
    return render(request, 'attendance/attendance_home.html')

# Session Management
@login_required
@user_passes_test(is_teacher_or_admin)
def session_list(request):
    if request.user.is_admin:
        sessions = Session.objects.all()
    else:  # Teacher
        sessions = Session.objects.filter(course__teacher=request.user)
    
    return render(request, 'attendance/session_list.html', {'sessions': sessions})

@login_required
@user_passes_test(is_teacher_or_admin)
def session_detail(request, pk):
    session = get_object_or_404(Session, pk=pk)
    
    # Check if user has permission to view this session
    if not request.user.is_admin and session.course.teacher != request.user:
        messages.error(request, "You don't have permission to view this session.")
        return redirect('session_list')
    
    attendance_records = AttendanceRecord.objects.filter(session=session)
    attendance_stats = {
        'total': attendance_records.count(),
        'present': attendance_records.filter(status=AttendanceRecord.AttendanceStatus.PRESENT).count(),
        'absent': attendance_records.filter(status=AttendanceRecord.AttendanceStatus.ABSENT).count(),
        'late': attendance_records.filter(status=AttendanceRecord.AttendanceStatus.LATE).count(),
        'excused': attendance_records.filter(status=AttendanceRecord.AttendanceStatus.EXCUSED).count(),
    }
    
    return render(request, 'attendance/session_detail.html', {
        'session': session,
        'attendance_records': attendance_records,
        'stats': attendance_stats
    })

@login_required
@user_passes_test(is_teacher_or_admin)
def session_create(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            
            # Check if user has permission to create session for this course
            if not request.user.is_admin and session.course.teacher != request.user:
                messages.error(request, "You don't have permission to create sessions for this course.")
                return redirect('session_list')
            
            session.save()
            
            # Auto-create attendance records for all students in the course
            for student in session.course.students.all():
                AttendanceRecord.objects.create(
                    student=student,
                    session=session,
                    status=AttendanceRecord.AttendanceStatus.ABSENT,
                    marked_by=request.user
                )
            
            messages.success(request, 'Session created successfully!')
            return redirect('session_detail', pk=session.pk)
    else:
        # Pre-fill the form based on user's role
        initial = {}
        if request.user.role == CustomUser.Role.TEACHER:
            courses = Course.objects.filter(teacher=request.user)
            if courses.exists():
                initial['course'] = courses.first()
        
        form = SessionForm(initial=initial)
        
        # Limit course choices for teachers
        if not request.user.is_admin:
            form.fields['course'].queryset = Course.objects.filter(teacher=request.user)
    
    return render(request, 'attendance/session_form.html', {'form': form})

@login_required
@user_passes_test(is_teacher_or_admin)
def session_update(request, pk):
    session = get_object_or_404(Session, pk=pk)
    
    # Check if user has permission to update this session
    if not request.user.is_admin and session.course.teacher != request.user:
        messages.error(request, "You don't have permission to update this session.")
        return redirect('session_list')
    
    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Session updated successfully!')
            return redirect('session_detail', pk=session.pk)
    else:
        form = SessionForm(instance=session)
        
        # Limit course choices for teachers
        if not request.user.is_admin:
            form.fields['course'].queryset = Course.objects.filter(teacher=request.user)
    
    return render(request, 'attendance/session_form.html', {'form': form, 'session': session})

@login_required
@user_passes_test(is_teacher_or_admin)
def session_delete(request, pk):
    session = get_object_or_404(Session, pk=pk)
    
    # Check if user has permission to delete this session
    if not request.user.is_admin and session.course.teacher != request.user:
        messages.error(request, "You don't have permission to delete this session.")
        return redirect('session_list')
    
    if request.method == 'POST':
        session.delete()
        messages.success(request, 'Session deleted successfully!')
        return redirect('session_list')
    
    return render(request, 'attendance/session_confirm_delete.html', {'session': session})

# Attendance Management
@login_required
@user_passes_test(is_teacher_or_admin)
def take_attendance(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    
    # Check if user has permission to take attendance for this session
    if not request.user.is_admin and session.course.teacher != request.user:
        messages.error(request, "You don't have permission to take attendance for this session.")
        return redirect('session_list')
    
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('student_'):
                student_id = key.split('_')[1]
                try:
                    student = CustomUser.objects.get(id=student_id, role=CustomUser.Role.STUDENT)
                    attendance_record, created = AttendanceRecord.objects.get_or_create(
                        student=student,
                        session=session,
                        defaults={'marked_by': request.user}
                    )
                    attendance_record.status = value
                    attendance_record.time_in = timezone.now() if value == AttendanceRecord.AttendanceStatus.PRESENT else None
                    attendance_record.marked_by = request.user
                    
                    # Save notes if provided
                    notes_key = f'notes_{student_id}'
                    if notes_key in request.POST:
                        attendance_record.comments = request.POST.get(notes_key)
                    
                    attendance_record.save()
                except CustomUser.DoesNotExist:
                    pass
        
        messages.success(request, 'Attendance recorded successfully!')
        return redirect('session_detail', pk=session.pk)
    
    # Get all students in this course
    students = session.course.students.all()
    attendance_records = {}
    
    for student in students:
        record, created = AttendanceRecord.objects.get_or_create(
            student=student,
            session=session,
            defaults={
                'status': AttendanceRecord.AttendanceStatus.ABSENT,
                'marked_by': request.user
            }
        )
        attendance_records[student.id] = record
    
    return render(request, 'attendance/take_attendance.html', {
        'session': session,
        'students': students,
        'attendance_records': attendance_records,
    })

@login_required
@user_passes_test(is_teacher_or_admin)
def barcode_attendance(request):
    if request.method == 'POST':
        form = BarcodeAttendanceForm(request.POST, teacher=request.user if not request.user.is_admin else None)
        if form.is_valid():
            barcode_id = form.cleaned_data['barcode_id']
            session = form.cleaned_data['session']
            
            try:
                student = CustomUser.objects.get(barcode_id=barcode_id, role=CustomUser.Role.STUDENT)
                
                # Check if student is enrolled in the course
                if student not in session.course.students.all():
                    messages.error(request, f"Error: Student {student.username} is not enrolled in this course.")
                    return redirect('barcode_attendance')
                
                # Create or update attendance record
                attendance_record, created = AttendanceRecord.objects.get_or_create(
                    student=student,
                    session=session,
                    defaults={
                        'status': AttendanceRecord.AttendanceStatus.PRESENT,
                        'time_in': timezone.now(),
                        'marked_by': request.user,
                        'marked_with': 'BARCODE'
                    }
                )
                
                if not created:
                    attendance_record.status = AttendanceRecord.AttendanceStatus.PRESENT
                    attendance_record.time_in = timezone.now()
                    attendance_record.marked_by = request.user
                    attendance_record.marked_with = 'BARCODE'
                    attendance_record.save()
                
                messages.success(request, f"Attendance marked for {student.get_full_name()} (ID: {student.barcode_id})")
                
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid barcode ID. No student found with this ID.")
            
            # Reset form
            form = BarcodeAttendanceForm(teacher=request.user if not request.user.is_admin else None)
    else:
        form = BarcodeAttendanceForm(teacher=request.user if not request.user.is_admin else None)
    
    return render(request, 'attendance/barcode_attendance.html', {'form': form})

# API for barcode scanning (for mobile apps)
@login_required
@user_passes_test(is_teacher_or_admin)
def api_mark_attendance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            barcode_id = data.get('barcode_id')
            session_id = data.get('session_id')
            
            if not barcode_id or not session_id:
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
            
            try:
                student = CustomUser.objects.get(barcode_id=barcode_id, role=CustomUser.Role.STUDENT)
                session = Session.objects.get(pk=session_id)
                
                # Check if student is enrolled in the course
                if student not in session.course.students.all():
                    return JsonResponse({
                        'status': 'error', 
                        'message': f"Student {student.username} is not enrolled in this course."
                    }, status=400)
                
                # Create or update attendance record
                attendance_record, created = AttendanceRecord.objects.get_or_create(
                    student=student,
                    session=session,
                    defaults={
                        'status': AttendanceRecord.AttendanceStatus.PRESENT,
                        'time_in': timezone.now(),
                        'marked_by': request.user,
                        'marked_with': 'BARCODE'
                    }
                )
                
                if not created:
                    attendance_record.status = AttendanceRecord.AttendanceStatus.PRESENT
                    attendance_record.time_in = timezone.now()
                    attendance_record.marked_by = request.user
                    attendance_record.marked_with = 'BARCODE'
                    attendance_record.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': f"Attendance marked for {student.get_full_name()}",
                    'student': {
                        'id': student.id,
                        'name': student.get_full_name(),
                        'username': student.username
                    },
                    'record_id': attendance_record.id  # Add record ID for deletion
                })
                
            except CustomUser.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid barcode ID'}, status=400)
            except Session.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid session ID'}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@login_required
@user_passes_test(is_admin)  # Only admin can delete records
def api_delete_attendance(request):
    """API endpoint for deleting attendance records (admin only)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            record_id = data.get('record_id')
            
            if not record_id:
                return JsonResponse({'status': 'error', 'message': 'Missing record ID'}, status=400)
            
            try:
                attendance_record = AttendanceRecord.objects.get(pk=record_id)
                
                # Store info for confirmation message
                student_name = attendance_record.student.get_full_name()
                session_date = attendance_record.session.date
                
                # Delete the record
                attendance_record.delete()
                
                return JsonResponse({
                    'status': 'success',
                    'message': f"Deleted attendance record for {student_name} on {session_date}",
                })
                
            except AttendanceRecord.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Attendance record not found'}, status=404)
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

# Reports
@login_required
@user_passes_test(is_teacher_or_admin)
def export_attendance(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    
    # Check if user has permission to export attendance for this session
    if not request.user.is_admin and session.course.teacher != request.user:
        messages.error(request, "You don't have permission to export attendance for this session.")
        return redirect('session_list')
    
    format_type = request.GET.get('format', 'csv')
    
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="attendance_{session.course.code}_{session.date}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Name', 'Status', 'Time In', 'Time Out', 'Marked By', 'Method', 'Comments'])
        
        attendance_records = AttendanceRecord.objects.filter(session=session)
        for record in attendance_records:
            writer.writerow([
                record.student.username,
                record.student.get_full_name(),
                record.get_status_display(),
                record.time_in.strftime('%Y-%m-%d %H:%M:%S') if record.time_in else '',
                record.time_out.strftime('%Y-%m-%d %H:%M:%S') if record.time_out else '',
                record.marked_by.get_full_name() if record.marked_by else '',
                record.get_marked_with_display(),
                record.comments or ''
            ])
        
        return response
    
    elif format_type == 'excel':
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Add headers
        headers = ['Student ID', 'Name', 'Status', 'Time In', 'Time Out', 'Marked By', 'Method', 'Comments']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)
        
        # Add data
        attendance_records = AttendanceRecord.objects.filter(session=session)
        for row_num, record in enumerate(attendance_records, 1):
            worksheet.write(row_num, 0, record.student.username)
            worksheet.write(row_num, 1, record.student.get_full_name())
            worksheet.write(row_num, 2, record.get_status_display())
            worksheet.write(row_num, 3, record.time_in.strftime('%Y-%m-%d %H:%M:%S') if record.time_in else '')
            worksheet.write(row_num, 4, record.time_out.strftime('%Y-%m-%d %H:%M:%S') if record.time_out else '')
            worksheet.write(row_num, 5, record.marked_by.get_full_name() if record.marked_by else '')
            worksheet.write(row_num, 6, record.get_marked_with_display())
            worksheet.write(row_num, 7, record.comments or '')
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="attendance_{session.course.code}_{session.date}.xlsx"'
        return response
    
    else:
        messages.error(request, "Invalid export format.")
        return redirect('session_detail', pk=session.pk)

@login_required
@user_passes_test(is_teacher_or_admin)
def face_attendance(request):
    """View for taking attendance using face recognition."""
    if request.method == 'POST':
        session_id = request.POST.get('session')
        image_data = request.POST.get('image_data')
        
        if not session_id or not image_data:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
        
        try:
            session = Session.objects.get(pk=session_id)
            
            # Process face recognition
            recognized_faces = face_recognition_system.recognize_from_base64(image_data)
            
            results = []
            for face in recognized_faces:
                try:
                    student = CustomUser.objects.get(pk=face['user_id'], role=CustomUser.Role.STUDENT)
                    
                    # Check if student is enrolled in the course
                    if student not in session.course.students.all():
                        results.append({
                            'name': face['name'],
                            'status': 'error',
                            'message': f"Student not enrolled in this course"
                        })
                        continue
                    
                    # Create or update attendance record
                    attendance_record, created = AttendanceRecord.objects.get_or_create(
                        student=student,
                        session=session,
                        defaults={
                            'status': AttendanceRecord.AttendanceStatus.PRESENT,
                            'time_in': timezone.now(),
                            'marked_by': request.user,
                            'marked_with': 'FACE'
                        }
                    )
                    
                    if not created:
                        attendance_record.status = AttendanceRecord.AttendanceStatus.PRESENT
                        attendance_record.time_in = timezone.now()
                        attendance_record.marked_by = request.user
                        attendance_record.marked_with = 'FACE'
                        attendance_record.save()
                    
                    results.append({
                        'name': face['name'],
                        'confidence': face['confidence'],
                        'status': 'success',
                        'message': 'Attendance marked'
                    })
                    
                except CustomUser.DoesNotExist:
                    results.append({
                        'name': face['name'],
                        'status': 'error',
                        'message': 'User not found in system'
                    })
            
            if not results:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No faces recognized'
                })
            
            return JsonResponse({
                'status': 'success',
                'recognized_count': len(results),
                'results': results
            })
            
        except Session.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid session ID'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    # For GET request, show the form with camera access
    form = BulkAttendanceForm(teacher=request.user if not request.user.is_admin else None)
    
    return render(request, 'attendance/face_attendance.html', {'form': form})

@login_required
def register_face(request):
    """View for registering a user's face."""
    # Check if we have a user_id in the query string (for admins)
    target_user = None
    url_user_id = request.GET.get('user_id')
    
    if url_user_id and request.user.is_admin:
        try:
            target_user = CustomUser.objects.get(id=url_user_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('face_management')
    
    if request.method == 'POST':
        image_data = request.POST.get('image_data')
        user_id = request.POST.get('user_id')
        
        if not image_data:
            messages.error(request, "No image data received")
            return redirect('register_face')
        
        # Determine which user to register the face for
        if user_id and request.user.is_admin:
            try:
                target_user = CustomUser.objects.get(id=user_id)
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found")
                return redirect('register_face')
        else:
            target_user = request.user
        
        # Process the face encoding
        success, message = face_recognition_system.add_face_encoding(target_user, image_data)
        
        if success:
            if target_user == request.user:
                messages.success(request, "Face registered successfully! Your face can now be used for attendance.")
            else:
                messages.success(request, f"Face registered successfully for {target_user.get_full_name()}!")
        else:
            messages.error(request, f"Error registering face: {message}")
        
        # Redirect based on user role and registration target
        if target_user != request.user:
            return redirect('face_management')
        elif request.user.is_student:
            return redirect('profile')
        else:
            return redirect('face_attendance')
    
    # Get list of users for admin selection
    users = None
    if request.user.is_admin:
        users = CustomUser.objects.all().order_by('role', 'username')
    
    # Check if user already has a face encoding
    has_face_encoding = target_user.face_encoding is not None if target_user else request.user.face_encoding is not None
    
    return render(request, 'attendance/register_face.html', {
        'has_face_encoding': has_face_encoding,
        'users': users,
        'is_admin': request.user.is_admin,
        'target_user': target_user
    })

@login_required
@user_passes_test(is_admin)
def face_management(request):
    """View for managing registered faces."""
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete':
            user_id = request.POST.get('user_id')
            try:
                user = CustomUser.objects.get(id=user_id)
                user.face_encoding = None
                user.save()
                messages.success(request, f"Face registration for {user.get_full_name()} has been deleted.")
            except CustomUser.DoesNotExist:
                messages.error(request, "User not found")
        
        elif action == 'bulk_delete':
            selected_users = request.POST.getlist('selected_users[]')
            if selected_users:
                count = 0
                for user_id in selected_users:
                    try:
                        user = CustomUser.objects.get(id=user_id)
                        if user.face_encoding is not None:
                            user.face_encoding = None
                            user.save()
                            count += 1
                    except CustomUser.DoesNotExist:
                        pass
                
                if count > 0:
                    messages.success(request, f"Face registrations for {count} users have been deleted.")
                else:
                    messages.warning(request, "No face registrations were deleted.")
            else:
                messages.warning(request, "No users were selected.")
        
        return redirect('face_management')
    
    # Get users with face encodings
    users_with_faces = CustomUser.objects.filter(face_encoding__isnull=False).order_by('role', 'username')
    
    # Get users without face encodings (for quick registration)
    users_without_faces = CustomUser.objects.filter(face_encoding__isnull=True).order_by('role', 'username')
    
    # Calculate statistics
    total_users = CustomUser.objects.count()
    total_with_faces = users_with_faces.count()
    total_without_faces = users_without_faces.count()
    
    stats = {
        'total_users': total_users,
        'total_with_faces': total_with_faces,
        'total_without_faces': total_without_faces,
        'percentage_registered': round((total_with_faces / total_users * 100) if total_users > 0 else 0, 1),
        
        # Role-specific stats
        'students_total': CustomUser.objects.filter(role=CustomUser.Role.STUDENT).count(),
        'students_registered': CustomUser.objects.filter(role=CustomUser.Role.STUDENT, face_encoding__isnull=False).count(),
        'teachers_total': CustomUser.objects.filter(role=CustomUser.Role.TEACHER).count(),
        'teachers_registered': CustomUser.objects.filter(role=CustomUser.Role.TEACHER, face_encoding__isnull=False).count(),
        'admins_total': CustomUser.objects.filter(role=CustomUser.Role.ADMIN).count(),
        'admins_registered': CustomUser.objects.filter(role=CustomUser.Role.ADMIN, face_encoding__isnull=False).count(),
    }
    
    return render(request, 'attendance/face_management.html', {
        'users_with_faces': users_with_faces,
        'users_without_faces': users_without_faces,
        'stats': stats
    })

@login_required
def global_search(request):
    """Global search functionality for the application."""
    query = request.GET.get('q', '')
    results = {
        'users': [],
        'courses': [],
        'sessions': [],
        'query': query
    }
    
    if query:
        # Search for users
        if request.user.is_admin:
            # Admins can search all users
            users = CustomUser.objects.filter(
                models.Q(username__icontains=query) |
                models.Q(first_name__icontains=query) |
                models.Q(last_name__icontains=query) |
                models.Q(email__icontains=query)
            )[:20]  # Limit to 20 results
            results['users'] = users
        elif request.user.is_teacher:
            # Teachers can only search students in their courses
            teacher_courses = Course.objects.filter(teacher=request.user)
            student_ids = []
            for course in teacher_courses:
                student_ids.extend(course.students.values_list('id', flat=True))
            
            users = CustomUser.objects.filter(id__in=student_ids).filter(
                models.Q(username__icontains=query) |
                models.Q(first_name__icontains=query) |
                models.Q(last_name__icontains=query)
            )[:20]
            results['users'] = users
        
        # Search for courses
        if request.user.is_admin:
            # Admins can search all courses
            courses = Course.objects.filter(
                models.Q(code__icontains=query) |
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query)
            )[:20]
        elif request.user.is_teacher:
            # Teachers can only search their own courses
            courses = Course.objects.filter(
                models.Q(code__icontains=query) |
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query),
                teacher=request.user
            )[:20]
        else:
            # Students can only search courses they're enrolled in
            courses = Course.objects.filter(
                models.Q(code__icontains=query) |
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query),
                students=request.user
            )[:20]
        
        results['courses'] = courses
        
        # Search for sessions
        if request.user.is_admin:
            # Admins can search all sessions
            sessions = Session.objects.filter(
                models.Q(course__code__icontains=query) |
                models.Q(course__name__icontains=query) |
                models.Q(description__icontains=query)
            )[:20]
        elif request.user.is_teacher:
            # Teachers can only search their own sessions
            sessions = Session.objects.filter(
                models.Q(course__code__icontains=query) |
                models.Q(course__name__icontains=query) |
                models.Q(description__icontains=query),
                course__teacher=request.user
            )[:20]
        else:
            # Students can only search sessions for courses they're enrolled in
            sessions = Session.objects.filter(
                models.Q(course__code__icontains=query) |
                models.Q(course__name__icontains=query) |
                models.Q(description__icontains=query),
                course__students=request.user
            )[:20]
        
        results['sessions'] = sessions
    
    return render(request, 'attendance/global_search.html', results)

@login_required
@user_passes_test(is_teacher_or_admin)
def barcode_scanner(request):
    """View for scanning barcodes via camera to mark attendance."""
    # Get active sessions for the dropdown
    today = timezone.now().date()
    
    if request.user.is_admin:
        # Admins can select from all active sessions
        active_sessions = Session.objects.filter(
            date__gte=today
        ).order_by('date', 'start_time')
    else:
        # Teachers can only select from their own sessions
        active_sessions = Session.objects.filter(
            date__gte=today,
            course__teacher=request.user
        ).order_by('date', 'start_time')
    
    context = {
        'active_sessions': active_sessions
    }
    
    return render(request, 'attendance/barcode_scanner.html', context)
