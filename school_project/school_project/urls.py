from django.urls import path
from attendance_app import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # API Paths - Authentication
    path('api/login/student/', views.student_login_api, name='api_student_login'),
    path('api/login/teacher/', views.teacher_login_api, name='api_teacher_login'),
    
    # API Paths - Student Management
    path('api/students/', views.get_students_api, name='api_get_students'),
    path('api/students/update/', views.update_student_api, name='api_update_student'),
    path('api/students/delete/', views.delete_student_api, name='api_delete_student'),
    
    # API Paths - Attendance
    path('api/attendance/mark/', views.mark_attendance_api, name='api_mark_attendance'),
    path('api/attendance/daily/', views.get_daily_attendance_api, name='api_daily_attendance'),
    path('api/attendance/upload/', views.upload_qr_image_api, name='api_upload_qr'),
]