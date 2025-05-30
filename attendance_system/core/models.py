from django.db import models
from django.utils.text import slugify
from users.models import CustomUser

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    head = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'role': CustomUser.Role.TEACHER}
    )
    
    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='courses_taught',
        limit_choices_to={'role': CustomUser.Role.TEACHER}
    )
    students = models.ManyToManyField(
        CustomUser, 
        related_name='enrolled_courses',
        limit_choices_to={'role': CustomUser.Role.STUDENT},
        blank=True
    )
    start_date = models.DateField()
    end_date = models.DateField()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
        
    class Meta:
        ordering = ['department', 'code']
