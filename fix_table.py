import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="feedbackdb"
)

cur = con.cursor()

# Add missing columns
cur.execute("ALTER TABLE students_feedback ADD COLUMN semester VARCHAR(10)")
cur.execute("ALTER TABLE students_feedback CHANGE class branch VARCHAR(30)")

con.commit()
con.close()

print("✅ Table fixed successfully!")
