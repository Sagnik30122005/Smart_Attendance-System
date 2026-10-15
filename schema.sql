-- ============================================
-- Zero-Trust Attendance System - Database Schema
-- ============================================

CREATE DATABASE IF NOT EXISTS attendance_db;
USE attendance_db;

-- 1. TEACHERS
CREATE TABLE IF NOT EXISTS teacher (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. STUDENTS
CREATE TABLE IF NOT EXISTS student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    device_hash VARCHAR(255) DEFAULT NULL,   -- locked device fingerprint (NULL until first login)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. COURSES
CREATE TABLE IF NOT EXISTS course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    teacher_id INT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teacher(id) ON DELETE CASCADE
);

-- 4. REGISTRATIONS (which students are enrolled in which course)
CREATE TABLE IF NOT EXISTS registration (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE,
    UNIQUE KEY unique_registration (student_id, course_id)
);

-- 5. SESSIONS (a single attendance window started by a teacher)
CREATE TABLE IF NOT EXISTS session (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    teacher_id INT NOT NULL,
    start_time DATETIME NOT NULL,
    teacher_ip VARCHAR(45) NOT NULL,
    window_seconds INT NOT NULL DEFAULT 35,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teacher(id) ON DELETE CASCADE
);

-- 6. ATTENDANCE (a successful check-in)
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    student_id INT NOT NULL,
    check_in_time DATETIME NOT NULL,
    student_ip VARCHAR(45) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'present',
    FOREIGN KEY (session_id) REFERENCES session(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
    UNIQUE KEY unique_attendance_per_session (session_id, student_id)   -- Constraint: one check-in per student per session
);

-- 7. SESSION LOG (rejected attempts - useful for debugging / catching proxy attempts)
CREATE TABLE IF NOT EXISTS session_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    student_id INT,
    attempted_at DATETIME NOT NULL,
    result VARCHAR(20) NOT NULL,     -- 'accepted' or 'rejected'
    reason VARCHAR(255),             -- why it was rejected
    FOREIGN KEY (session_id) REFERENCES session(id) ON DELETE CASCADE
);
