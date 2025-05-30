from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'barcode_id', 'phone_number', 'profile_pic')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'barcode_id', 'phone_number', 'profile_pic')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Pre-authenticate to get the user object, but don't complete login yet
            self.user_cache = authenticate(self.request, username=username, password=password)
            
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                # Teacher-specific area checks
                is_teacher_area = any(
                    teacher_area in self.request.GET.get('next', '')
                    for teacher_area in ['/sessions/create/', '/take-attendance/']
                )
                if is_teacher_area and self.user_cache.role not in [CustomUser.Role.ADMIN, CustomUser.Role.TEACHER]:
                    raise ValidationError(
                        "TEACHER/ADMIN LOGIN ONLY: Students cannot access this area.",
                        code='teacher_only'
                    )
                
                self.confirm_login_allowed(self.user_cache)
                
        return self.cleaned_data

class AdminAuthenticationForm(AuthenticationForm):
    """Authentication form specifically for administrators"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admin Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Admin Password'}))
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Pre-authenticate to get the user object
            self.user_cache = authenticate(self.request, username=username, password=password)
            
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                # Only allow admin users
                if self.user_cache.role != CustomUser.Role.ADMIN:
                    raise ValidationError(
                        "Administrator access only. Your account does not have administrator privileges.",
                        code='not_admin'
                    )
                
                self.confirm_login_allowed(self.user_cache)
                
        return self.cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'profile_pic')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }

class BarcodeRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('barcode_id',)
        widgets = {
            'barcode_id': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        }
    
    def clean_barcode_id(self):
        barcode_id = self.cleaned_data.get('barcode_id')
        if barcode_id:
            if CustomUser.objects.filter(barcode_id=barcode_id).exclude(id=self.instance.id).exists():
                raise ValidationError("This barcode ID is already in use.")
        return barcode_id 