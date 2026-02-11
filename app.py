import os
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, session
import mysql.connector
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


app = Flask(__name__)
app.secret_key = "feedback_secret_key"


# ---------- DB CONNECTION ----------


def db():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE"),
        port=int(os.environ.get("MYSQLPORT")),
        ssl_disabled=False
    )


con = db()
cur = con.cursor()


# ---------- LOAD SUBJECTS ----------
@app.route("/get_subjects")
def get_subjects():
    branch = request.args.get("branch")
    year = request.args.get("year")
    semester = request.args.get("semester")
    section = request.args.get("section")

    con = db()
    cur = con.cursor()
    cur.execute("""
        SELECT subject_name, faculty_name
        FROM subjects
        WHERE branch=%s AND year=%s AND semester=%s AND section=%s
    """, (branch, year, semester, section))
    rows = cur.fetchall()
    con.close()

    return jsonify({
        "subjects": [{"subject": r[0], "faculty": r[1]} for r in rows]
    })


# ---------- STUDENT LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        con = db()
        cur = con.cursor()

        # Auto create student
        cur.execute("SELECT role FROM users WHERE username=%s", (username,))
        user = cur.fetchone()

        if not user:
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (%s,%s,'student')",
                (username, username)
            )
            con.commit()

        cur.execute(
            "SELECT role FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()
        con.close()

        if user and user[0] == "student":
            session["user"] = username
            return redirect(url_for("student_page"))

        return "Invalid Student Login"

    return render_template("login_student.html")


# ---------- STUDENT PAGE ----------
@app.route("/student", methods=["GET", "POST"])
def student_page():
    if "user" not in session:
        return redirect(url_for("student_login"))

    if request.method == "POST":
        data = request.form
        con = db()
        cur = con.cursor()

        # Prevent duplicate feedback
        cur.execute("""
            SELECT id FROM students_feedback
            WHERE login_id=%s AND subject=%s
        """, (session["user"], data['subject']))

        if cur.fetchone():
            con.close()
            return "<h3>You have already submitted feedback for this subject.</h3>"

        # Insert feedback
        cur.execute("""
            INSERT INTO students_feedback
            (name, roll, year, semester, branch, section, subject, suggestion, login_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            data['name'],
            session["user"],
            data['year'],
            data['semester'],
            data['branch'],
            data['section'],
            data['subject'],
            data.get('suggestion'),
            session["user"]
        ))

        fid = cur.lastrowid
        answers = [int(data[f"q{i}"]) for i in range(1, 11)]

        cur.execute("""
            INSERT INTO answers
            (feedback_id,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (fid, *answers))

        con.commit()
        con.close()
        return "<h2>Feedback Submitted Successfully</h2>"

    return render_template("student.html", roll=session["user"])


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("student_login"))


# ---------- ADMIN LOGIN ----------
@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        con = db()
        cur = con.cursor()
        cur.execute(
            "SELECT role FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()
        con.close()

        if user and user[0] == "admin":
            session["admin"] = username
            return redirect(url_for("admin"))

        return "Invalid Admin Login"

    return render_template("login_admin.html")


@app.route("/admin_logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


# ---------- ADMIN DASHBOARD ----------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "admin" not in session:
        return redirect(url_for("admin_login"))

    percentage = 0
    responses = 0
    students = []

    if request.method == "POST":
        year = request.form["year"]
        semester = request.form["semester"]
        branch = request.form["branch"]
        section = request.form["section"]
        subject = request.form["subject"]

        con = db()
        cur = con.cursor()

        cur.execute("""
            SELECT a.q1,a.q2,a.q3,a.q4,a.q5,
                   a.q6,a.q7,a.q8,a.q9,a.q10,
                   s.suggestion,
                   s.login_id
            FROM answers a
            JOIN students_feedback s ON a.feedback_id = s.id
            WHERE s.year=%s AND s.semester=%s
            AND s.branch=%s AND s.section=%s
            AND s.subject=%s
        """, (year, semester, branch, section, subject))

        rows = cur.fetchall()
        responses = len(rows)
        suggestions = []

        if responses > 0:
            total = sum(sum(r[:10]) for r in rows)
            percentage = (total / (50 * responses)) * 100
            suggestions = [r[10] for r in rows if r[10]]
            students = [r[11] for r in rows]

        cur.execute("""
            SELECT faculty_name FROM subjects
            WHERE branch=%s AND year=%s AND semester=%s
            AND section=%s AND subject_name=%s
        """, (branch, year, semester, section, subject))

        row = cur.fetchone()
        faculty = row[0] if row else ""
        con.close()

        # Save for PDF
        session["report_data"] = {
            "rows": [r[:10] for r in rows],
            "info": (year, semester, branch, section, subject, faculty),
            "responses": responses,
            "percentage": percentage,
            "suggestions": suggestions
        }

    return render_template("admin.html",
                           percentage=percentage,
                           responses=responses,
                           students=students)

@app.route("/report")
def report():
    data = session.get("report_data")
    if not data:
        return "Generate report first"

    rows = data["rows"]
    year, semester, branch, section, subject, faculty = data["info"]
    responses = data["responses"]
    suggestions = data.get("suggestions", [])
    percentage = data["percentage"]

    # -------- Count ratings --------
    counts = [[0]*5 for _ in range(10)]
    for row in rows:
        for i, val in enumerate(row):
            counts[i][val-1] += 1

    file = "feedback_report.pdf"
    doc = SimpleDocTemplate(
        file, pagesize=A4,
        rightMargin=20, leftMargin=20,
        topMargin=20, bottomMargin=20
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------- HEADER ----------
    logo_path = os.path.join(app.root_path, 'static', 'logo.png')
    img = Image(logo_path, width=55, height=55)
    img.hAlign = 'CENTER'
    elements.append(img)
    elements.append(Spacer(1, 6))

    elements.append(Paragraph(
        "<b><font size=18 color='blue'>MALLA REDDY COLLEGE OF ENGINEERING</font></b>",
        styles['Title']
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("<b>Feedback Form Report</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))

    # ---------- INFO TABLE ----------
    info = [
        ["Branch", branch, "Year", year, "Semester", semester],
        ["Section", section, "Subject", subject, "Faculty", faculty],
        ["Responses", str(responses), "", "", ""]
    ]

    t = Table(info, colWidths=[55,50,55,170,100])


    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 10))

    # ---------- PERCENTAGE ----------
    elements.append(Paragraph(
        f"<b>Overall Feedback Percentage: {percentage:.2f}%</b>",
        styles['Normal']
    ))
    elements.append(Spacer(1, 10))

    # ---------- QUESTIONS TABLE ----------
    questions = [
        "Teacher comes to the class in time",
        "Teacher comes well planned and prepared",
        "Teacher speaks clearly and audibly",
        "Teacher provides examples effectively",
        "Use of ICT tools while teaching",
        "Teacher encourages doubts and answers well",
        "Teacher is courteous and impartial",
        "Teacher maintains discipline",
        "Teacher completes syllabus at proper pace",
        "Teacher gives feedback on answer scripts"
    ]

    table_data = [[Paragraph("<b>Criteria</b>", styles['Normal']),
                   "5","4","3","2","1","Total"]]

    for i, q in enumerate(questions):
        total = sum(counts[i])
        table_data.append([
            Paragraph(q, styles['Normal']),
            counts[i][4], counts[i][3],
            counts[i][2], counts[i][1],
            counts[i][0], total
        ])

    table = Table(table_data, colWidths=[165,30,30,30,30,30,40])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # ---------- SUGGESTIONS ----------
    if suggestions:
        elements.append(Paragraph("<b>Student Suggestions</b>", styles['Heading3']))
        elements.append(Spacer(1, 6))
        for i, s in enumerate(suggestions, 1):
            elements.append(Paragraph(f"{i}. {s}", styles['Normal']))
            elements.append(Spacer(1, 4))

    # ---------- FLEXIBLE SPACE BEFORE SIGNATURE ----------
    elements.append(Spacer(1, 80))

    # ---------- SIGNATURE TABLE ----------
    sign_table = Table(
        [["HOD Signature", "", "Principal Signature"],
         ["", "", ""]],
        colWidths=[220, 80, 220]
    )
    sign_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('LINEABOVE', (0,1), (0,1), 1, colors.black),
        ('LINEABOVE', (2,1), (2,1), 1, colors.black),
    ]))

    elements.append(sign_table)

    doc.build(elements)
    return send_file(file, as_attachment=True)



# ---------- RESET ----------
@app.route("/reset_feedback")
def reset_feedback():
    con = db()
    cur = con.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    cur.execute("TRUNCATE TABLE answers")
    cur.execute("TRUNCATE TABLE students_feedback")
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    con.commit()
    con.close()
    return "All Feedback Reset Successfully!"


if __name__ == "__main__":
    app.run(debug=True)
