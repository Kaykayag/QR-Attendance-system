from django.db import models
from django.utils import timezone
import datetime

class Student(models.Model):
    # Matches your frontend requirements
    student_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    level = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_qr_data(self):
        return f"STUDENT:{self.student_id}"

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.subject})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class DailyAttendance(models.Model):
    """Daily attendance records - one record per student per day"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, blank=True)
    time_marked = models.TimeField(auto_now_add=True)
    is_present = models.BooleanField(default=False)
    marked_by_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    qr_scanned = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date', 'student__last_name']
    
    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student.student_id} - {self.date} - {status}"

class AttendanceLog(models.Model):
    """Log of all attendance marking activities"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now, blank=True)
    time_marked = models.TimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=[
        ('QR_SCAN', 'QR Code Scan'),
        ('MANUAL', 'Manual Entry'),
        ('BULK', 'Bulk Import'),
    ])
    qr_data = models.CharField(max_length=100, blank=True)
    success = models.BooleanField(default=True)
    message = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-date', '-time_marked']
    
    def __str__(self):
        return f"{self.student.student_id} - {self.date} - {self.method}"