# QR Attendance System - Setup & Running Guide

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Navigate to Project Directory
```bash
cd QR-Attendance-system/school_project
```

### Step 2: Install Dependencies
```bash
pip install django
```

### Step 3: Apply Database Migrations
```bash
python manage.py migrate
```

### Step 4: Start the Development Server
```bash
python manage.py runserver
```

### Step 5: Access the Application
Open your web browser and go to: **http://127.0.0.1:8000/**

---

## 📱 How to Use the QR Attendance System

### For Students:

1. **Student Registration**
   - Click "Student Portal" on the landing page
   - Fill in your details:
     - First Name and Last Name
     - Student ID Number (e.g., 23746944)
     - Course and Level
   - Click "Generate Pass"

2. **Digital ID Card**
   - Your digital ID card will be displayed
   - It contains your QR code with format: `STUDENT:{YOUR_ID}`
   - Save or screenshot your QR code for attendance

### For Teachers:

1. **Teacher Registration**
   - Click "Teacher Portal" on the landing page
   - Fill in your details:
     - First Name and Last Name
     - Teacher ID Number
     - Subject you're teaching
   - Click "Access Dashboard"

2. **Attendance Management**
   - View real-time statistics (Present, Total Students, Attendance Rate)
   - **Camera Scan**: Use device camera to scan QR codes
   - **Upload Image**: Upload QR code images from gallery
   - **Manage Students**: View, edit, and manage student records

3. **Scanning Process**
   - Click "Camera Scan" or "Upload Image"
   - Scan or upload student QR code
   - System automatically marks student as present
   - View attendance log in real-time

---

## 🔧 Technical Features

### Database Models
- **Students**: Auto-saved to database with unique IDs
- **Teachers**: Subject-based teacher management
- **Daily Attendance**: Fresh attendance records each day
- **Attendance Logs**: Complete audit trail

### QR Code System
- **Format**: `STUDENT:{student_id}` (e.g., STUDENT:23746944)
- **Generation**: Automatic based on student registration
- **Validation**: Smart extraction and matching
- **Duplicate Prevention**: One attendance per student per day

### API Endpoints
- `POST /api/login/student/` - Student registration
- `POST /api/login/teacher/` - Teacher login
- `GET /api/students/` - Get all students
- `POST /api/attendance/mark/` - Mark attendance
- `GET /api/attendance/daily/` - Daily statistics

---

## 🛠️ Troubleshooting

### Common Issues:

1. **Server won't start**
   - Make sure you're in the correct directory: `QR-Attendance-system/school_project`
   - Check Python version: `python --version`
   - Install Django: `pip install django`

2. **Database errors**
   - Run migrations: `python manage.py migrate`
   - Delete `db.sqlite3` and migrate again if needed

3. **Camera not working**
   - Allow camera permissions in your browser
   - Use HTTPS for camera access (localhost is allowed)

4. **QR scanning issues**
   - Ensure good lighting
   - Hold QR code steady
   - Try uploading image if camera fails

### Development Commands:
```bash
# Make database changes
python manage.py makemigrations attendance_app
python manage.py migrate

# Create superuser (for admin)
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

---

## 📂 Project Structure

```
QR-Attendance-system/
└── school_project/
    ├── manage.py                 # Django management script
    ├── db.sqlite3               # SQLite database
    ├── school_project/          # Project configuration
    │   ├── settings.py         # Django settings
    │   ├── urls.py            # URL routing
    │   └── ...
    └── attendance_app/         # Main application
        ├── models.py          # Database models
        ├── views.py           # API endpoints
        ├── templates/         # HTML templates
        ├── migrations/        # Database migrations
        └── static/           # CSS, JS files
```

---

## 🎯 Key Workflows

### Student Registration Flow:
1. Student fills form → 2. Auto-save to DB → 3. Generate QR → 4. Display ID card

### Teacher Attendance Flow:
1. Teacher login → 2. Open scanner → 3. Scan QR → 4. Mark present → 5. Update logs

### Daily Process:
1. Fresh attendance records created each day
2. Prevents duplicate attendance marking
3. Real-time statistics and reporting

---

## 🚀 Production Deployment

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper `ALLOWED_HOSTS`
3. Use PostgreSQL or MySQL instead of SQLite
4. Set up proper static file serving
5. Configure HTTPS and security headers
6. Set up proper backup strategy

---

**System Requirements**: Modern web browser with JavaScript enabled
**Supported Platforms**: Windows, macOS, Linux
**Database**: SQLite (development) / PostgreSQL (production)
**Framework**: Django 4.2.27