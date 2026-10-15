"""
Zero-Trust Attendance System - Flask Backend
==============================================
Implements:
  Phase 1: Core infrastructure (login, start session, check-in)
  Phase 2: Device-level security (fingerprint lock)
  Phase 3: Time-based security (35 second window)
  Phase 4: Network-level security (subnet match)
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import datetime

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"   # used to keep users logged in

# ---------- DATABASE CONNECTION ----------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",         
    "password": "Sagnik@123",          
    "database": "attendance_db",
    "cursorclass": pymysql.cursors.DictCursor,
}

def get_db():
    return pymysql.connect(**DB_CONFIG)

# The attendance window length, in seconds (Phase 3 - from your notes)
ATTENDANCE_WINDOW_SECONDS = 35


# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")


# ================= TEACHER: REGISTER / LOGIN =================
@app.route("/teacher/register", methods=["GET", "POST"])
def teacher_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        pw_hash = generate_password_hash(password)

        db = get_db()
        try:
            with db.cursor() as cur:
                cur.execute(
                    "INSERT INTO teacher (name, email, password_hash) VALUES (%s, %s, %s)",
                    (name, email, pw_hash),
                )
            db.commit()
            flash("Teacher account created. Please log in.")
            return redirect(url_for("teacher_login"))
        except pymysql.err.IntegrityError:
            flash("That email is already registered.")
        finally:
            db.close()
    return render_template("teacher_register.html")


@app.route("/teacher/login", methods=["GET", "POST"])
def teacher_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        with db.cursor() as cur:
            cur.execute("SELECT * FROM teacher WHERE email=%s", (email,))
            teacher = cur.fetchone()
        db.close()

        if teacher and check_password_hash(teacher["password_hash"], password):
            session["teacher_id"] = teacher["id"]
            session["teacher_name"] = teacher["name"]
            return redirect(url_for("teacher_dashboard"))
        flash("Invalid email or password.")
    return render_template("teacher_login.html")


@app.route("/teacher/dashboard")
def teacher_dashboard():
    if "teacher_id" not in session:
        return redirect(url_for("teacher_login"))

    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM course WHERE teacher_id=%s", (session["teacher_id"],))
        courses = cur.fetchall()
    db.close()
    return render_template("teacher_dashboard.html", courses=courses)


@app.route("/teacher/course/create", methods=["POST"])
def create_course():
    if "teacher_id" not in session:
        return redirect(url_for("teacher_login"))

    name = request.form["name"]
    code = request.form["code"]

    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO course (name, code, teacher_id) VALUES (%s, %s, %s)",
            (name, code, session["teacher_id"]),
        )
    db.commit()
    db.close()
    return redirect(url_for("teacher_dashboard"))


# ---------- Phase 1 + 3 + 4: START SESSION ----------
@app.route("/teacher/session/start", methods=["POST"])
def start_session():
    if "teacher_id" not in session:
        return jsonify({"error": "not logged in"}), 401

    try:
        course_id = request.form["course_id"]
        teacher_id = session["teacher_id"]
        teacher_ip = request.remote_addr

        db = get_db()

        with db.cursor() as cur:
            cur.execute(
                """INSERT INTO session
                   (course_id, teacher_id, start_time, teacher_ip, window_seconds, is_active)
                   VALUES (%s, %s, %s, %s, %s, TRUE)""",
                (
                    course_id,
                    teacher_id,
                    datetime.datetime.now(),
                    teacher_ip,
                    ATTENDANCE_WINDOW_SECONDS
                )
            )

            session_id = cur.lastrowid

        db.commit()
        db.close()

        print("SESSION CREATED:", session_id)

        return jsonify({
            "success": True,
            "session_id": session_id,
            "window_seconds": ATTENDANCE_WINDOW_SECONDS,
            "teacher_ip": teacher_ip
        })

    except Exception as e:
        print("SESSION START ERROR:", str(e))

        try:
            db.close()
        except:
            pass

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ================= STUDENT: REGISTER / LOGIN =================
@app.route("/student/register", methods=["GET", "POST"])
def student_register():
    if request.method == "POST":
        name = request.form["name"]
        roll_no = request.form["roll_no"]
        email = request.form["email"]
        password = request.form["password"]
        pw_hash = generate_password_hash(password)

        db = get_db()
        try:
            with db.cursor() as cur:
                cur.execute(
                    "INSERT INTO student (name, roll_no, email, password_hash) VALUES (%s, %s, %s, %s)",
                    (name, roll_no, email, pw_hash),
                )
            db.commit()
            flash("Student account created. Please log in.")
            return redirect(url_for("student_login"))
        except pymysql.err.IntegrityError:
            flash("That email or roll number is already registered.")
        finally:
            db.close()
    return render_template("student_register.html")


@app.route("/student/login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        with db.cursor() as cur:
            cur.execute("SELECT * FROM student WHERE email=%s", (email,))
            student = cur.fetchone()
        db.close()

        if student and check_password_hash(student["password_hash"], password):
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            return redirect(url_for("student_dashboard"))
        flash("Invalid email or password.")
    return render_template("student_login.html")


@app.route("/student/dashboard")
def student_dashboard():
    if "student_id" not in session:
        return redirect(url_for("student_login"))

    db = get_db()
    with db.cursor() as cur:
        cur.execute("""
            SELECT c.id, c.name, c.code FROM course c
            JOIN registration r ON r.course_id = c.id
            WHERE r.student_id = %s
        """, (session["student_id"],))
        courses = cur.fetchall()
    db.close()
    return render_template("student_dashboard.html", courses=courses)


@app.route("/student/enroll", methods=["POST"])
def enroll():
    if "student_id" not in session:
        return redirect(url_for("student_login"))
    code = request.form["code"]

    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT id FROM course WHERE code=%s", (code,))
        course = cur.fetchone()
        if course:
            try:
                cur.execute(
                    "INSERT INTO registration (student_id, course_id) VALUES (%s, %s)",
                    (session["student_id"], course["id"]),
                )
                db.commit()
            except pymysql.err.IntegrityError:
                flash("Already enrolled in that course.")
        else:
            flash("No course found with that code.")
    db.close()
    return redirect(url_for("student_dashboard"))


# ---------- Phase 2 + 3 + 4: CHECK-IN (the core security logic) ----------
@app.route("/student/checkin", methods=["POST"])
def checkin():
    if "student_id" not in session:
        return jsonify({"error": "not logged in"}), 401

    data = request.get_json()
    session_id = data.get("session_id")
    fingerprint = data.get("fingerprint")   # from FingerprintJS on the frontend
    student_id = session["student_id"]
    student_ip = request.remote_addr

    db = get_db()
    with db.cursor() as cur:

        # --- Fetch the session ---
        cur.execute("SELECT * FROM session WHERE id=%s", (session_id,))
        att_session = cur.fetchone()
        if not att_session or not att_session["is_active"]:
            db.close()
            return jsonify({"status": "rejected", "reason": "Session not active"}), 400

        # --- CHECK A: TIME (Phase 3) ---
        elapsed = (datetime.datetime.now() - att_session["start_time"]).total_seconds()
        if elapsed > att_session["window_seconds"]:
            _log(db, session_id, student_id, "rejected", "Time window expired")
            db.close()
            return jsonify({"status": "rejected", "reason": "Attendance window closed"}), 400

        # --- CHECK B: DEVICE FINGERPRINT (Phase 2) ---
        cur.execute("SELECT device_hash FROM student WHERE id=%s", (student_id,))
        student = cur.fetchone()

        if student["device_hash"] is None:
            # First time this student checks in -> lock their device
            cur.execute("UPDATE student SET device_hash=%s WHERE id=%s", (fingerprint, student_id))
            db.commit()
        elif student["device_hash"] != fingerprint:
            _log(db, session_id, student_id, "rejected", "Device fingerprint mismatch")
            db.close()
            return jsonify({"status": "rejected", "reason": "This isn't your registered device"}), 400

        # --- CHECK C: NETWORK / SUBNET (Phase 4) ---
        if not _same_subnet(att_session["teacher_ip"], student_ip):
            _log(db, session_id, student_id, "rejected", "Different network/subnet")
            db.close()
            return jsonify({"status": "rejected", "reason": "You must be on the same network as the teacher"}), 400

        # --- ALL CHECKS PASSED -> MARK PRESENT ---
        try:
            cur.execute(
                """INSERT INTO attendance (session_id, student_id, check_in_time, student_ip, status)
                   VALUES (%s, %s, %s, %s, 'present')""",
                (session_id, student_id, datetime.datetime.now(), student_ip),
            )
            db.commit()
            _log(db, session_id, student_id, "accepted", "All checks passed")
        except pymysql.err.IntegrityError:
            db.close()
            return jsonify({"status": "rejected", "reason": "You already checked in for this session"}), 400

    db.close()
    return jsonify({"status": "accepted"})


def _same_subnet(ip1, ip2):
    """Phase 4: compare the first three octets (Class-C style /24 subnet check)."""
    # localhost testing helper: treat 127.0.0.1 as always matching itself
    if ip1 == ip2:
        return True
    try:
        parts1 = ip1.split(".")[:3]
        parts2 = ip2.split(".")[:3]
        return parts1 == parts2
    except Exception:
        return False


def _log(db, session_id, student_id, result, reason):
    with db.cursor() as cur:
        cur.execute(
            """INSERT INTO session_log (session_id, student_id, attempted_at, result, reason)
               VALUES (%s, %s, %s, %s, %s)""",
            (session_id, student_id, datetime.datetime.now(), result, reason),
        )
    db.commit()


# ---------- View who's present in a session (teacher side) ----------
@app.route("/teacher/session/<int:session_id>/attendance")
def view_attendance(session_id):
    if "teacher_id" not in session:
        return redirect(url_for("teacher_login"))

    db = get_db()
    with db.cursor() as cur:
        cur.execute("""
            SELECT s.name, s.roll_no, a.check_in_time, a.student_ip
            FROM attendance a JOIN student s ON s.id = a.student_id
            WHERE a.session_id = %s
        """, (session_id,))
        records = cur.fetchall()
    db.close()
    return render_template("attendance_view.html", records=records, session_id=session_id)


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
