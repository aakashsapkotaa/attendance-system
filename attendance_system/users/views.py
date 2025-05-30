from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomAuthenticationForm, AdminAuthenticationForm, UserProfileForm, BarcodeRegistrationForm
from django.contrib import messages
from core.models import Course, Department
from attendance.models import Session, AttendanceRecord
from django.http import HttpResponseRedirect
from django.db import models

def is_admin(user):
    return user.is_authenticated and user.role == CustomUser.Role.ADMIN

def is_teacher_or_admin(user):
    return user.is_authenticated and user.role in [CustomUser.Role.ADMIN, CustomUser.Role.TEACHER]

class CustomLoginView(LoginView):
    """Regular login view for students and teachers"""
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        # If trying to access admin areas, redirect to admin login
        next_url = request.GET.get('next', '')
        if 'admin_dashboard' in next_url or '/admin/' in next_url:
            return redirect('admin_login')
            
        # If user is already authenticated
        if request.user.is_authenticated:
            # Teacher area check
            is_teacher_area = any(area in next_url for area in ['/sessions/create/', '/take-attendance/'])
            if is_teacher_area and request.user.role == CustomUser.Role.STUDENT:
                messages.error(request, "Access denied. Only teachers and administrators can access this area.")
                return redirect('dashboard')
        
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Process valid form submission."""
        # Get the authenticated user
        user = form.get_user()
        next_url = self.request.GET.get('next', '')
        
        # Check if accessing teacher areas but not a teacher/admin
        if any(area in next_url for area in ['/sessions/create/', '/take-attendance/']) and \
           user.role not in [CustomUser.Role.ADMIN, CustomUser.Role.TEACHER]:
            form.add_error(None, "Access denied. Only teachers and administrators can access this area.")
            messages.error(self.request, "Access denied. Only teachers and administrators can access this area.")
            return self.form_invalid(form)
        
        # If it's an admin, and they want to go to admin areas, let them
        if user.role == CustomUser.Role.ADMIN and ('admin_dashboard' in next_url or '/admin/' in next_url):
            return super().form_valid(form)
            
        # If all checks pass, proceed with login
        return super().form_valid(form)

class AdminLoginView(LoginView):
    """Specialized login view for administrators only"""
    form_class = AdminAuthenticationForm
    template_name = 'users/admin_login.html'
    
    def dispatch(self, request, *args, **kwargs):
        # If already logged in as admin, proceed
        if request.user.is_authenticated and request.user.role == CustomUser.Role.ADMIN:
            return super().dispatch(request, *args, **kwargs)
            
        # If already logged in as non-admin, redirect with error
        if request.user.is_authenticated:
            messages.error(request, "You don't have administrator privileges. Please log out and log in as an administrator.")
            return redirect('landing_page')
            
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        """Return the URL to redirect to after successful login."""
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('admin_dashboard')

@login_required
def dashboard(request):
    # Enforce role-based access
    if request.user.is_admin:
        return redirect('admin_dashboard')
    
    # Check request path to ensure proper role access
    request_path = request.path
    
    # Prevent student from accessing teacher areas
    if request.user.role == CustomUser.Role.STUDENT and '/teacher/' in request_path:
        messages.error(request, "Access denied. Students cannot access teacher areas.")
        return redirect('dashboard')
    
    # Prevent teacher from accessing admin areas
    if request.user.role == CustomUser.Role.TEACHER and '/admin/' in request_path:
        messages.error(request, "Access denied. Teachers cannot access admin areas.")
        return redirect('dashboard')
    
    context = {}
    
    # Teacher dashboard data
    if request.user.is_teacher:
        context['recent_sessions'] = Session.objects.filter(
            course__teacher=request.user
        ).order_by('-date')[:5]
    
    return render(request, 'users/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Explicitly check if the user is admin, redirect if not
    if not request.user.is_admin:
        messages.error(request, "Access denied. Only administrators can access this area.")
        return redirect('landing_page')
    
    # User statistics
    user_count = CustomUser.objects.count()
    admin_count = CustomUser.objects.filter(role=CustomUser.Role.ADMIN).count()
    teacher_count = CustomUser.objects.filter(role=CustomUser.Role.TEACHER).count()
    student_count = CustomUser.objects.filter(role=CustomUser.Role.STUDENT).count()
    
    # Course and department counts
    course_count = Course.objects.count()
    department_count = Department.objects.count()
    session_count = Session.objects.count()
    
    # Attendance statistics
    present_count = AttendanceRecord.objects.filter(status=AttendanceRecord.AttendanceStatus.PRESENT).count()
    absent_count = AttendanceRecord.objects.filter(status=AttendanceRecord.AttendanceStatus.ABSENT).count()
    late_count = AttendanceRecord.objects.filter(status=AttendanceRecord.AttendanceStatus.LATE).count()
    excused_count = AttendanceRecord.objects.filter(status=AttendanceRecord.AttendanceStatus.EXCUSED).count()
    
    # Recent data
    recent_users = CustomUser.objects.all().order_by('-date_joined')[:5]
    recent_sessions = Session.objects.all().order_by('-date')[:5]
    
    context = {
        'user_count': user_count,
        'admin_count': admin_count,
        'teacher_count': teacher_count,
        'student_count': student_count,
        'course_count': course_count,
        'department_count': department_count,
        'session_count': session_count,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'excused_count': excused_count,
        'recent_users': recent_users,
        'recent_sessions': recent_sessions,
    }
    
    return render(request, 'users/admin_dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})

@login_required
def barcode_registration(request):
    if request.method == 'POST':
        form = BarcodeRegistrationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your barcode ID has been updated!')
            return redirect('profile')
    else:
        form = BarcodeRegistrationForm(instance=request.user)
    
    return render(request, 'users/barcode_registration.html', {'form': form})

@user_passes_test(is_admin)
def user_list(request):
    search_query = request.GET.get('q', '')
    role_filter = request.GET.get('role', '')
    
    users = CustomUser.objects.all()
    
    # Apply search if provided
    if search_query:
        users = users.filter(
            models.Q(username__icontains=search_query) |
            models.Q(first_name__icontains=search_query) |
            models.Q(last_name__icontains=search_query) |
            models.Q(email__icontains=search_query)
        )
    
    # Apply role filter if provided
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Count by role
    admin_count = users.filter(role=CustomUser.Role.ADMIN).count()
    teacher_count = users.filter(role=CustomUser.Role.TEACHER).count()
    student_count = users.filter(role=CustomUser.Role.STUDENT).count()
    
    context = {
        'users': users,
        'search_query': search_query,
        'role_filter': role_filter,
        'admin_count': admin_count,
        'teacher_count': teacher_count,
        'student_count': student_count,
    }
    
    return render(request, 'users/user_list.html', context)

@user_passes_test(is_admin)
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})

class UserCreateView(UserPassesTestMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'User created successfully!')
        return super().form_valid(form)

class UserUpdateView(UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully!')
        return super().form_valid(form)

@login_required
def user_search(request):
    """Search functionality for the user panel."""
    query = request.GET.get('q', '')
    results = {
        'courses': [],
        'sessions': [],
        'query': query,
        'user_is_teacher_or_admin': is_teacher_or_admin(request.user)
    }
    
    if query:
        # Search for courses based on user role
        if request.user.is_admin:
            # Admins can search all courses
            results['courses'] = Course.objects.filter(
                models.Q(code__icontains=query) |
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query)
            )[:10]
        elif request.user.is_teacher:
            # Teachers can only search their own courses
            results['courses'] = Course.objects.filter(
                models.Q(code__icontains=query) |
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query),
                teacher=request.user
            )[:10]
        else:
            # Students can only search courses they're enrolled in
            results['courses'] = Course.objects.filter(
                models.Q(code__icontains=query) |
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query),
                students=request.user
            )[:10]
        
        # Search for sessions based on user role
        if request.user.is_admin:
            # Admins can search all sessions
            results['sessions'] = Session.objects.filter(
                models.Q(course__code__icontains=query) |
                models.Q(course__name__icontains=query) |
                models.Q(description__icontains=query)
            )[:10]
        elif request.user.is_teacher:
            # Teachers can only search their own sessions
            results['sessions'] = Session.objects.filter(
                models.Q(course__code__icontains=query) |
                models.Q(course__name__icontains=query) |
                models.Q(description__icontains=query),
                course__teacher=request.user
            )[:10]
        else:
            # Students can only search sessions for courses they're enrolled in
            results['sessions'] = Session.objects.filter(
                models.Q(course__code__icontains=query) |
                models.Q(course__name__icontains=query) |
                models.Q(description__icontains=query),
                course__students=request.user
            )[:10]
        
        # Add attendance records for students
        if request.user.is_student:
            results['attendance_records'] = AttendanceRecord.objects.filter(
                models.Q(session__course__code__icontains=query) |
                models.Q(session__course__name__icontains=query),
                student=request.user
            )[:20]
    
    return render(request, 'users/user_search.html', results)

@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    """View for admin users to delete user accounts."""
    user = get_object_or_404(CustomUser, pk=pk)
    
    # Prevent admins from deleting themselves
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user_detail', pk=pk)
    
    if request.method == 'POST':
        # Store info for success message
        username = user.username
        full_name = user.get_full_name()
        
        # Delete the user
        user.delete()
        
        messages.success(request, f"User '{username}' ({full_name}) has been deleted successfully.")
        return redirect('user_list')
    
    return render(request, 'users/user_confirm_delete.html', {'user': user})
