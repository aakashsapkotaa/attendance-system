from django.urls import path
from . import views

urlpatterns = [
    # Root path
    path('', views.attendance_home, name='attendance_home'),
    
    # Session management
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/<int:pk>/', views.session_detail, name='session_detail'),
    path('sessions/create/', views.session_create, name='session_create'),
    path('sessions/<int:pk>/update/', views.session_update, name='session_update'),
    path('sessions/<int:pk>/delete/', views.session_delete, name='session_delete'),
    
    # Attendance management
    path('sessions/<int:session_id>/take-attendance/', views.take_attendance, name='take_attendance'),
    path('barcode-attendance/', views.barcode_attendance, name='barcode_attendance'),
    path('barcode-scanner/', views.barcode_scanner, name='barcode_scanner'),
    path('face-attendance/', views.face_attendance, name='face_attendance'),
    path('register-face/', views.register_face, name='register_face'),
    path('face-management/', views.face_management, name='face_management'),
    
    # Search
    path('search/', views.global_search, name='global_search'),
    
    # API
    path('api/mark-attendance/', views.api_mark_attendance, name='api_mark_attendance'),
    path('api/delete-attendance/', views.api_delete_attendance, name='api_delete_attendance'),
    
    # Reports
    path('sessions/<int:session_id>/export/', views.export_attendance, name='export_attendance'),
] 