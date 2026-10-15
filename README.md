# 🔐 Zero-Trust Attendance System

A secure, web-based attendance management system built using **Flask, MySQL, HTML, CSS, and JavaScript**.

The system follows a **Zero-Trust approach** where every attendance request is validated before marking a student present. It supports separate **Teacher and Student portals**, time-limited attendance sessions, course enrollment, live attendance monitoring, and database-backed attendance records.

---

## 📌 Project Overview

Traditional attendance systems often depend on manual roll calls or simple attendance links. Such systems can be vulnerable to problems such as:

- Proxy attendance
- Late attendance submissions
- Unauthorized access
- Students checking into invalid sessions
- Lack of proper attendance logs
- Difficulty monitoring attendance in real time

The **Zero-Trust Attendance System** addresses these issues by validating every attendance request against multiple conditions before accepting it.

The system provides:

- Teacher registration and login
- Student registration and login
- Course creation
- Student course enrollment
- Teacher-controlled attendance sessions
- Time-limited attendance windows
- Student check-in
- Attendance validation
- Live attendance monitoring
- IP address logging
- Session attempt logging
- MySQL database storage

---

# 🎯 Objectives

The main objectives of the project are:

1. Build a centralized digital attendance system.
2. Provide separate authentication for teachers and students.
3. Allow teachers to create and manage courses.
4. Allow students to enroll in courses using course codes.
5. Allow teachers to start temporary attendance sessions.
6. Restrict attendance to a predefined time window.
7. Validate student attendance requests before accepting them.
8. Maintain detailed attendance records in MySQL.
9. Provide teachers with live attendance monitoring.
10. Maintain logs of both successful and rejected attendance attempts.

---

# 🏗️ System Architecture

The system follows a basic three-layer architecture:

```text
                    ┌──────────────────────┐
                    │      Web Browser     │
                    │   Student / Teacher  │
                    └──────────┬───────────┘
                               │
                               │ HTTP Requests
                               ▼
                    ┌──────────────────────┐
                    │     Flask Backend    │
                    │       app.py         │
                    │                      │
                    │ Authentication       │
                    │ Course Management     │
                    │ Session Management    │
                    │ Attendance Validation │
                    │ Security Checks       │
                    └──────────┬───────────┘
                               │
                               │ SQL Queries
                               ▼
                    ┌──────────────────────┐
                    │     MySQL Database   │
                    │    attendance_db     │
                    │                      │
                    │ Students             │
                    │ Teachers             │
                    │ Courses              │
                    │ Sessions             │
                    │ Attendance           │
                    │ Session Logs         │
                    └──────────────────────┘
````

---

# 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* Flask
* Werkzeug

### Database

* MySQL
* MySQL Workbench

### Development Tools

* Visual Studio Code
* Python Virtual Environment
* Google Chrome

---

# 📂 Project Structure

```text
Attendance System/
│
└── attendance_system/
    │
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── schema.sql
    │
    ├── venv/
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   │
    │   └── js/
    │       └── student.js
    │
    └── templates/
        ├── index.html
        ├── student_login.html
        ├── student_register.html
        ├── student_dashboard.html
        ├── teacher_login.html
        ├── teacher_register.html
        ├── teacher_dashboard.html
        └── attendance_view.html
```

---

# 👥 User Roles

The application has two primary user roles.

## 👨‍🏫 Teacher

Teachers can:

* Register an account
* Login securely
* Create courses
* Generate course codes
* View their courses
* Start attendance sessions
* Control the attendance window
* View live attendance
* Monitor student check-ins

---

## 👨‍🎓 Student

Students can:

* Register an account
* Login securely
* Enroll in courses
* View available course functionality
* Enter an attendance session ID
* Check in to an active attendance session
* Receive success or rejection messages

---

# 🔑 Authentication

The system provides separate authentication mechanisms for teachers and students.

Passwords are not stored directly as plain text.

The backend uses password hashing functionality provided by Werkzeug.

Conceptually:

```text
User Password
      │
      ▼
Password Hashing
      │
      ▼
Stored Hash
      │
      ▼
Login Attempt
      │
      ▼
Hash Verification
      │
      ├── Correct → Login successful
      │
      └── Incorrect → Login rejected
```

---

# 📚 Course Management

Teachers can create courses using:

```text
Course Name
Course Code
```

For example:

```text
Course Name: DBMS
Course Code: 301205
```

The generated course code can then be shared with students.

Students use the course code to enroll in the course.

---

# 🕒 Attendance Session

A teacher can start an attendance session for a course.

Each attendance session receives a unique session ID.

For example:

```text
Session #4
```

The session also has a predefined attendance window.

In the tested implementation:

```text
Attendance Window = 35 seconds
```

The session is stored in the database together with information such as:

* Session ID
* Course ID
* Teacher ID
* Start time
* Teacher IP
* Attendance window
* Active status

---

# 🔄 Attendance Workflow

The complete attendance workflow is:

```text
Teacher Login
      │
      ▼
Teacher Dashboard
      │
      ▼
Select Course
      │
      ▼
Start Attendance Session
      │
      ▼
Unique Session ID Generated
      │
      ▼
Teacher Shares Session ID
      │
      ▼
Student Enters Session ID
      │
      ▼
Attendance Validation
      │
      ├───────────────┐
      │               │
      ▼               ▼
 Valid Request     Invalid Request
      │               │
      ▼               ▼
Attendance        Rejection
Recorded          + Log Entry
      │
      ▼
Live Attendance Page
      │
      ▼
MySQL Database
```

---

# 🛡️ Zero-Trust Attendance Validation

The system follows a Zero-Trust principle.

Instead of automatically trusting a student's attendance request, every request is validated.

The request must satisfy the required conditions before attendance is recorded.

Conceptually:

```text
Student Check-In Request
          │
          ▼
    Session Exists?
          │
       Yes │ No
          │   └──> Reject
          ▼
    Session Active?
          │
       Yes │ No
          │   └──> Reject
          ▼
 Attendance Window Valid?
          │
       Yes │ No
          │   └──> Reject
          ▼
 Student Eligible?
          │
       Yes │ No
          │   └──> Reject
          ▼
     All Checks Passed
          │
          ▼
   Mark Student Present
```

This prevents the system from blindly accepting attendance requests.

---

# ⏱️ Time-Based Security

Attendance sessions are only valid for a limited period.

For example:

```text
Session Window = 35 seconds
```

If a student attempts to check in after the allowed window, the system rejects the request.

Example:

```text
Rejected: Attendance window closed
```

This helps prevent students from submitting attendance after the session has ended.

---

# 📡 Live Attendance Monitoring

Teachers can open the live attendance page for a particular session.

Example:

```text
Attendance for Session #4
```

The page automatically refreshes every few seconds.

It displays information such as:

| Field         | Description         |
| ------------- | ------------------- |
| Name          | Student name        |
| Roll No       | Student roll number |
| Check-in Time | Time of attendance  |
| IP            | Student IP address  |

Example:

```text
Name:          SAGNIK KUNDU
Roll No:       24051322
Check-in Time: 2026-09-24 17:15:06
IP:            127.0.0.1
```

---

# 🗄️ Database

The project uses MySQL with the database:

```text
attendance_db
```

The system maintains separate tables for different types of information.

Important tables include:

```text
students
teachers
courses
session
attendance
session_log
```

---

# 📊 Attendance Table

The attendance table stores successful attendance records.

Example structure:

```text
id
session_id
student_id
check_in_time
student_ip
status
```

Example record:

```text
id:            1
session_id:    4
student_id:    54
student_ip:    127.0.0.1
status:        present
```

---

# 📝 Session Logging

The system also maintains a log of attendance attempts.

This is important because both successful and unsuccessful attempts can be recorded.

Example:

```text
Session ID    Student ID    Result      Reason
-----------------------------------------------------------
2             54            rejected    Time window expired
4             54            accepted    All checks passed
```

This provides an audit trail for attendance requests.

---

# 🔍 Testing Performed

The system has been tested using both successful and unsuccessful attendance attempts.

## Test 1 — Teacher Login

```text
Result: PASS
```

Teacher successfully logs into the teacher dashboard.

---

## Test 2 — Student Login

```text
Result: PASS
```

Student successfully logs into the student dashboard.

---

## Test 3 — Course Creation

Example:

```text
Course: DBMS
Code: 301205
```

```text
Result: PASS
```

The course appears on the teacher dashboard.

---

## Test 4 — Attendance Session Creation

Example:

```text
Session #4
Window: 35 seconds
```

```text
Result: PASS
```

The session was successfully created and stored in MySQL.

---

## Test 5 — Live Attendance Page

The teacher can open:

```text
Attendance for Session #4
```

```text
Result: PASS
```

The live attendance page loads correctly.

---

## Test 6 — Successful Student Check-In

The student enters the correct session ID during the active attendance window.

Result:

```text
All checks passed
```

Attendance is recorded.

```text
Result: PASS
```

---

## Test 7 — Expired Attendance Window

A student attempted to check in after the allowed attendance window.

The system returned:

```text
Rejected: Attendance window closed
```

The attempt was also stored in the session log.

```text
Result: PASS
```

---

## Test 8 — Database Verification

The successful attendance record was found in MySQL.

Example:

```text
session_id = 4
student_id = 54
status = present
```

```text
Result: PASS
```

---

# 🧪 Example Test Flow

A complete successful test can be performed as follows:

### Step 1

Login as a teacher.

### Step 2

Open the teacher dashboard.

### Step 3

Create or select a course.

Example:

```text
DBMS
301205
```

### Step 4

Start an attendance session.

Example:

```text
Session #4
Window: 35 seconds
```

### Step 5

Login as a student.

### Step 6

Enter the session ID:

```text
4
```

### Step 7

Click:

```text
Check In Now
```

### Step 8

The request is validated.

### Step 9

The teacher's live attendance page updates.

### Step 10

Verify the attendance record in MySQL.

---

# ⚙️ Installation

## 1. Clone or Download the Project

Place the project on your computer.

Example:

```text
Attendance System/
└── attendance_system/
```

---

## 2. Open the Project in VS Code

Open the `attendance_system` folder in Visual Studio Code.

---

## 3. Create/Use the Virtual Environment

If the virtual environment already exists:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 4. Install Dependencies

With the virtual environment activated:

```powershell
pip install -r requirements.txt
```

---

# 🗃️ MySQL Setup

Make sure MySQL Server is installed and running.

Open MySQL Workbench and connect to:

```text
localhost:3306
```

Create/use the database:

```text
attendance_db
```

The database schema can be initialized using:

```text
schema.sql
```

---

# ▶️ Running the Application

Open the VS Code terminal inside:

```text
attendance_system
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Then start the Flask application:

```powershell
python app.py
```

The server should start at:

```text
http://127.0.0.1:5000
```

Open the URL in Google Chrome.

---

# 🖥️ Application Pages

The application contains pages for:

```text
Home
Student Login
Student Registration
Student Dashboard
Teacher Login
Teacher Registration
Teacher Dashboard
Live Attendance
```

---

# 🔐 Security Features

The project implements several security-oriented features:

### 1. Password Hashing

Passwords are stored using secure password hashing rather than plain text.

### 2. Session-Based Authentication

Users must authenticate before accessing protected dashboards.

### 3. Time-Limited Attendance

Attendance sessions automatically become invalid after the configured time window.

### 4. Session Validation

Attendance requests are associated with a specific session ID.

### 5. IP Logging

The system records the IP address associated with attendance attempts.

### 6. Attempt Logging

Both accepted and rejected attendance attempts can be recorded.

### 7. Database Persistence

Attendance and session information is stored persistently in MySQL.

---

# 📈 Future Improvements

The current system provides the core Zero-Trust attendance functionality. Future versions could include:

* Device fingerprinting
* Browser/device identification
* Stronger network/subnet validation
* QR-code based attendance
* Dynamic QR codes
* Geolocation-based validation
* Face recognition
* Multi-factor authentication
* Teacher attendance reports
* Student attendance percentage
* Export attendance to Excel/CSV
* Attendance analytics dashboard
* Email notifications
* Admin dashboard
* Cloud deployment
* HTTPS/TLS deployment
* Production-grade WSGI server
* Role-based access control
* Rate limiting
* Duplicate check-in prevention
* Attendance history for students

---

# ⚠️ Current Development Environment

This project is currently designed as a local development application.

The Flask development server is used for testing:

```text
http://127.0.0.1:5000
```

For production deployment, a production WSGI server and HTTPS should be used.

---

# 📌 Limitations

The current local implementation has some limitations:

* The application currently runs on a local machine.
* `127.0.0.1` is used during local testing.
* The current attendance window is configured for testing.
* Production-level HTTPS deployment is not yet configured.
* Advanced device fingerprinting and biometric verification are future enhancements.

---

# 🏆 Project Outcome

The implemented system successfully demonstrates the complete attendance lifecycle:

```text
Teacher Authentication
        ↓
Course Creation
        ↓
Student Enrollment
        ↓
Attendance Session Creation
        ↓
Unique Session ID
        ↓
Time-Based Validation
        ↓
Student Check-In
        ↓
Attendance Verification
        ↓
Live Attendance Display
        ↓
MySQL Storage
        ↓
Session Audit Logging
```

The system successfully handles both:

```text
VALID ATTENDANCE
       ↓
All checks passed
       ↓
Attendance recorded
```

and:

```text
INVALID ATTENDANCE
       ↓
Time window expired
       ↓
Attendance rejected
       ↓
Attempt logged
```

---

# 👨‍💻 Project Type

**Academic / Educational Project**

### Domain

```text
Web Development
Cybersecurity
Attendance Management
Database Management
Zero-Trust Security
```

---

# 📜 License

This project is developed for educational and academic purposes.
