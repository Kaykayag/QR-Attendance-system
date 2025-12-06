from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.utils import timezone
from .models import Student, Teacher, DailyAttendance, AttendanceLog
import json
import datetime
import re

def index(request):
    return render(request, 'attendance_app/index.html')

# ============ STUDENT API ENDPOINTS ============

@csrf_exempt
def student_login_api(request):
    """Enhanced student registration with auto-DB save and QR generation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['id', 'firstname', 'lastname', 'course', 'level']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'status': 'error', 'message': f'Missing field: {field}'}, status=400)
            
            # Create or Update the student in the Real DB
            with transaction.atomic():
                student, created = Student.objects.update_or_create(
                    student_id=data['id'],
                    defaults={
                        'first_name': data['firstname'],
                        'last_name': data['lastname'],
                        'course': data['course'],
                        'level': data['level'],
                        'is_active': True
                    }
                )
                
                # Create today's attendance record if it doesn't exist
                today = timezone.now().date()
                daily_attendance, _ = DailyAttendance.objects.get_or_create(
                    student=student,
                    date=today
                )
                
                action = 'Registered' if created else 'Updated'
                return JsonResponse({
                    'status': 'success', 
                    'message': f'Student {action} Successfully',
                    'student': {
                        'id': student.student_id,
                        'name': student.get_full_name(),
                        'course': student.course,
                        'level': student.level,
                        'qr_data': student.get_qr_data(),
                        'created': created
                    }
                })
                
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# ============ TEACHER API ENDPOINTS ============

@csrf_exempt
def teacher_login_api(request):
    """Enhanced teacher login"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['id', 'firstname', 'lastname', 'subject']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({'status': 'error', 'message': f'Missing field: {field}'}, status=400)
            
            # Create or Update the teacher in the Real DB
            teacher, created = Teacher.objects.update_or_create(
                teacher_id=data['id'],
                defaults={
                    'first_name': data['firstname'],
                    'last_name': data['lastname'],
                    'subject': data['subject'],
                    'is_active': True
                }
            )
            
            action = 'Registered' if created else 'Updated'
            return JsonResponse({
                'status': 'success', 
                'message': f'Teacher {action} Successfully',
                'teacher': {
                    'id': teacher.teacher_id,
                    'name': teacher.get_full_name(),
                    'subject': teacher.subject
                }
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# ============ STUDENT MANAGEMENT ENDPOINTS ============

@csrf_exempt
def get_students_api(request):
    """Get all students for teacher management"""
    if request.method == 'GET':
        try:
            students = Student.objects.filter(is_active=True).order_by('last_name', 'first_name')
            students_data = []
            
            for student in students:
                # Get today's attendance status
                today = timezone.now().date()
                daily_attendance = DailyAttendance.objects.filter(student=student, date=today).first()
                
                students_data.append({
                    'id': student.student_id,
                    'name': student.get_full_name(),
                    'course': student.course,
                    'level': student.level,
                    'created_at': student.created_at.isoformat(),
                    'is_present_today': daily_attendance.is_present if daily_attendance else False
                })
            
            return JsonResponse({
                'status': 'success',
                'students': students_data,
                'total': len(students_data)
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def update_student_api(request):
    """Update student information"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            
            if not student_id:
                return JsonResponse({'status': 'error', 'message': 'Student ID is required'}, status=400)
            
            student = get_object_or_404(Student, student_id=student_id)
            
            # Update student information
            if 'firstname' in data:
                student.first_name = data['firstname']
            if 'lastname' in data:
                student.last_name = data['lastname']
            if 'course' in data:
                student.course = data['course']
            if 'level' in data:
                student.level = data['level']
            if 'is_active' in data:
                student.is_active = data['is_active']
            
            student.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Student updated successfully',
                'student': {
                    'id': student.student_id,
                    'name': student.get_full_name(),
                    'course': student.course,
                    'level': student.level
                }
            })
            
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_student_api(request):
    """Delete/deactivate student"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            
            if not student_id:
                return JsonResponse({'status': 'error', 'message': 'Student ID is required'}, status=400)
            
            student = get_object_or_404(Student, student_id=student_id)
            student.is_active = False
            student.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Student deactivated successfully'
            })
            
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# ============ ATTENDANCE ENDPOINTS ============

def extract_student_id_from_qr(qr_data):
    """Extract student ID from QR code data"""
    if not qr_data:
        return None
    
    # Try to extract from "STUDENT:ID" format
    if qr_data.startswith('STUDENT:'):
        return qr_data.split('STUDENT:')[1]
    
    # Try to extract numeric ID directly
    numeric_match = re.search(r'\d+', qr_data)
    if numeric_match:
        return numeric_match.group()
    
    return None

@csrf_exempt
def mark_attendance_api(request):
    """Enhanced attendance marking with QR scanning"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            qr_data = data.get('qr_data', '')
            teacher_id = data.get('teacher_id', '')
            
            # Extract student ID from QR data
            student_id = extract_student_id_from_qr(qr_data)
            
            if not student_id:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'Invalid QR code format. Expected STUDENT:ID format.'
                }, status=400)
            
            # Find the student
            try:
                student = Student.objects.get(student_id=student_id, is_active=True)
            except Student.DoesNotExist:
                return JsonResponse({
                    'status': 'error', 
                    'message': f'Student ID {student_id} not found in database.'
                }, status=404)
            
            # Get or create teacher
            teacher = None
            if teacher_id:
                try:
                    teacher = Teacher.objects.get(teacher_id=teacher_id, is_active=True)
                except Teacher.DoesNotExist:
                    pass
            
            # Get today's date
            today = timezone.now().date()
            
            # Get or create daily attendance record
            daily_attendance, created = DailyAttendance.objects.get_or_create(
                student=student,
                date=today,
                defaults={'marked_by_teacher': teacher, 'qr_scanned': True}
            )
            
            # Check if already marked present
            if daily_attendance.is_present:
                return JsonResponse({
                    'status': 'warning',
                    'message': f'{student.get_full_name()} is already marked present today.',
                    'student': {
                        'name': student.get_full_name(),
                        'id': student.student_id,
                        'course_level': f"{student.course} - Year {student.level}",
                        'time_marked': daily_attendance.time_marked.strftime('%H:%M:%S')
                    }
                })
            
            # Mark as present
            daily_attendance.is_present = True
            daily_attendance.marked_by_teacher = teacher
            daily_attendance.qr_scanned = True
            daily_attendance.save()
            
            # Log the attendance
            AttendanceLog.objects.create(
                student=student,
                teacher=teacher,
                date=today,
                method='QR_SCAN',
                qr_data=qr_data,
                success=True,
                message='Attendance marked via QR scan'
            )
            
            return JsonResponse({
                'status': 'success',
                'message': f'✅ {student.get_full_name()} marked present!',
                'student': {
                    'name': student.get_full_name(),
                    'id': student.student_id,
                    'course_level': f"{student.course} - Year {student.level}",
                    'time_marked': daily_attendance.time_marked.strftime('%H:%M:%S')
                }
            })
            
        except Exception as e:
            # Log the failed attempt
            try:
                if 'student' in locals() and student:
                    AttendanceLog.objects.create(
                        student=student,
                        date=timezone.now().date(),
                        method='QR_SCAN',
                        qr_data=data.get('qr_data', ''),
                        success=False,
                        message=f'Error: {str(e)}'
                    )
            except:
                pass  # Don't fail the response if logging fails
            
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def get_daily_attendance_api(request):
    """Get today's attendance records"""
    if request.method == 'GET':
        try:
            today = timezone.now().date()
            attendance_records = DailyAttendance.objects.filter(date=today).select_related('student')
            
            records = []
            for record in attendance_records:
                records.append({
                    'student_id': record.student.student_id,
                    'student_name': record.student.get_full_name(),
                    'course_level': f"{record.student.course} - Year {record.student.level}",
                    'is_present': record.is_present,
                    'time_marked': record.time_marked.strftime('%H:%M:%S'),
                    'method': 'QR Scan' if record.qr_scanned else 'Manual'
                })
            
            # Get statistics
            total_students = Student.objects.filter(is_active=True).count()
            present_count = sum(1 for record in records if record['is_present'])
            absent_count = total_students - present_count
            
            return JsonResponse({
                'status': 'success',
                'date': today.isoformat(),
                'records': records,
                'statistics': {
                    'total_students': total_students,
                    'present': present_count,
                    'absent': absent_count,
                    'attendance_rate': round((present_count / total_students * 100) if total_students > 0 else 0, 2)
                }
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def upload_qr_image_api(request):
    """Upload and process QR image for attendance - This is now handled client-side by jsQR"""
    if request.method == 'POST':
        try:
            # Debug logging
            print(f"[DEBUG] upload_qr_image_api called with method: {request.method}")
            print(f"[DEBUG] Content-Type: {request.META.get('CONTENT_TYPE', 'Not set')}")
            print(f"[DEBUG] Request body: {request.body}")
            
            data = json.loads(request.body)
            qr_data = data.get('qr_data', '')
            teacher_id = data.get('teacher_id', '')
            
            print(f"[DEBUG] Parsed data - qr_data: {qr_data}, teacher_id: {teacher_id}")
            
            if not qr_data:
                return JsonResponse({'status': 'error', 'message': 'No QR data provided. Please ensure the image contains a valid QR code.'}, status=400)
            
            # Create a mock request object for the mark_attendance_api
            class MockRequest:
                def __init__(self, qr_data, teacher_id):
                    self.method = 'POST'
                    self.body = json.dumps({'qr_data': qr_data, 'teacher_id': teacher_id}).encode('utf-8')
            
            mock_request = MockRequest(qr_data, teacher_id)
            return mark_attendance_api(mock_request)
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON Decode Error: {str(e)}")
            print(f"[ERROR] Raw body content: {request.body}")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            print(f"[ERROR] General Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': f'Error processing QR image: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)