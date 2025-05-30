"""
URL configuration for attendance_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, landing_page
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('dashboard/', home, name='home'),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    # Add a redirect for URLs without trailing slash
    re_path(r'^users$', RedirectView.as_view(url='/users/', permanent=True)),
    path('attendance/', include('attendance.urls')),
    
    # Redirect admin dashboard directly to admin login
    path('users/admin-dashboard/', RedirectView.as_view(url='/users/admin-login/', query_string=True), name='admin_dashboard_redirect'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
