import mysql.connector

con = mysql.connector.connect(
    host="centerbeam.proxy.rlwy.net",
    user="root",
    password="OsLJHhJqgnJxdeTjuyUEZzYFOksChhHN",
    database="railway",
    port=46155,
    ssl_disabled=False
)

cur = con.cursor()

cur.execute("""
UPDATE users
SET password='admin123'
WHERE username='admin'
""")

con.commit()
print("Admin password reset")
