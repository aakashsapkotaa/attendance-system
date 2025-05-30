from django import forms
from .models import Session, AttendanceRecord
from users.models import CustomUser
from core.models import Course
from django.utils import timezone

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['course', 'date', 'start_time', 'end_time', 'description', 'is_active']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['student', 'session', 'status', 'comments']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'session': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BulkAttendanceForm(forms.Form):
    session = forms.ModelChoiceField(
        queryset=Session.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            # Only show active sessions for courses taught by this teacher
            self.fields['session'].queryset = Session.objects.filter(
                course__teacher=teacher,
                is_active=True
            )
        else:
            # Show all active sessions for admin users
            self.fields['session'].queryset = Session.objects.filter(is_active=True)

class BarcodeAttendanceForm(forms.Form):
    barcode_id = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Scan barcode or enter ID',
            'autofocus': True,
            'autocomplete': 'off'
        })
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        if teacher:
            # Only show active sessions for courses taught by this teacher
            self.fields['session'].queryset = Session.objects.filter(
                course__teacher=teacher,
                is_active=True
            )
    
    def clean_barcode_id(self):
        barcode_id = self.cleaned_data.get('barcode_id')
        try:
            student = CustomUser.objects.get(barcode_id=barcode_id, role=CustomUser.Role.STUDENT)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Invalid barcode ID. No student found with this ID.")
        return barcode_id 