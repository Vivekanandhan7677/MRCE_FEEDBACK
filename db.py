import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
cur = con.cursor()

# ------------------ CREATE DATABASE ------------------
cur.execute("CREATE DATABASE IF NOT EXISTS feedbackdb")
cur.execute("USE feedbackdb")
print("✅ Database ready")

# ------------------ DROP OLD TABLES ------------------
cur.execute("SET FOREIGN_KEY_CHECKS = 0")
cur.execute("DROP TABLE IF EXISTS answers")
cur.execute("DROP TABLE IF EXISTS students_feedback")
cur.execute("DROP TABLE IF EXISTS subjects")
cur.execute("DROP TABLE IF EXISTS users")
cur.execute("SET FOREIGN_KEY_CHECKS = 1")
print("✅ Old tables removed")

# ------------------ USERS TABLE ------------------
cur.execute("""
CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50),
    role VARCHAR(20)
)
""")

cur.execute("""
INSERT INTO users (username, password, role)
VALUES ('admin', 'admin123', 'admin')
""")

print("✅ users table created")

# ------------------ SUBJECTS TABLE ------------------
cur.execute("""
CREATE TABLE subjects(
    id INT AUTO_INCREMENT PRIMARY KEY,
    branch VARCHAR(30),
    year VARCHAR(10),
    semester VARCHAR(10),
    section VARCHAR(5),
    subject_name VARCHAR(255),
    faculty_name VARCHAR(255)
)
""")

print("✅ subjects table created")

# ------------------ STUDENTS FEEDBACK TABLE (UPDATED) ------------------
cur.execute("""
CREATE TABLE students_feedback(
    id INT AUTO_INCREMENT PRIMARY KEY,
    login_id VARCHAR(50),   -- ⭐ VERY IMPORTANT
    name VARCHAR(100),
    roll VARCHAR(50),
    year VARCHAR(10),
    semester VARCHAR(10),
    branch VARCHAR(30),
    section VARCHAR(5),
    subject VARCHAR(255),
    suggestion TEXT
)
""")
print("✅ students_feedback table created")

# ------------------ ANSWERS TABLE ------------------
cur.execute("""
CREATE TABLE answers(
    id INT AUTO_INCREMENT PRIMARY KEY,
    feedback_id INT,
    q1 INT, q2 INT, q3 INT, q4 INT, q5 INT,
    q6 INT, q7 INT, q8 INT, q9 INT, q10 INT,
    FOREIGN KEY (feedback_id)
    REFERENCES students_feedback(id)
    ON DELETE CASCADE
)
""")
print("✅ answers table created")

# ------------------ INSERT SUBJECTS ------------------
# ⚠️ KEEP YOUR SAME subjects_data LIST HERE (no changes)

# ------------------ INSERT SUBJECTS DATA ------------------
subjects_data = [
    # ---- KEEP YOUR BIG subjects_data LIST EXACTLY HERE ----
    
# SECTION A
("CSE_AI_ML", "II", "II", "A", "Discrete Mathematics", "Mrs. P. Bhuvaneswari"),
("CSE_AI_ML", "II", "II", "A", "Automata Theory & Compiler Design", "Mr. R. Venkatesh"),
("CSE_AI_ML", "II", "II", "A", "Database Management System", "Mr. G. Bharath Kumar Goud"),
("CSE_AI_ML", "II", "II", "A", "Introduction to Artificial Intelligence", "Mr. S. Mannivanan"),
("CSE_AI_ML", "II", "II", "A", "Object Oriented Programming through Java", "Mrs. G. Soumya"),
("CSE_AI_ML", "II", "II", "A", "Database Management System Lab", "Mr. G. Bharath Kumar"),
("CSE_AI_ML", "II", "II", "A", "Java Programming Lab", "Mr. S. Manikandan"),
("CSE_AI_ML", "II", "II", "A", "Real Time Research Project", "Mr. G. Bharath Kumar Goud"),
("CSE_AI_ML", "II", "II", "A", "PROLOG / LISP / PYSWIP", "Mrs. Anju Gopi"),

# SECTION B
("CSE_AI_ML", "II", "II", "B", "Discrete Mathematics", "Mrs. P. Bhuvaneswari"),
("CSE_AI_ML", "II", "II", "B", "Automata Theory & Compiler Design", "Mrs. K. Sunanda Reddy"),
("CSE_AI_ML", "II", "II", "B", "Database Management System", "Mrs. Rajee Josan"),
("CSE_AI_ML", "II", "II", "B", "Introduction to Artificial Intelligence", "Dr. V. Vivekanandhan"),
("CSE_AI_ML", "II", "II", "B", "Object Oriented Programming through Java", "Mrs. Shiva Priya"),
("CSE_AI_ML", "II", "II", "B", "Database Management System Lab", "Mr. G. Bharath Kumar"),
("CSE_AI_ML", "II", "II", "B", "Java Programming Lab", "Mrs. Shiva Priya"),
("CSE_AI_ML", "II", "II", "B", "Real Time Research Project", "Mrs. Shiva Priya"),
("CSE_AI_ML", "II", "II", "B", "PROLOG / LISP / PYSWIP", "Mr. S. Manivanan"),

("CSE_AI_ML","II","II","C","Discrete Mathematics","Mrs. P. Bhuvaneswari"),
("CSE_AI_ML","II","II","C","Automata Theory & Compiler Design","Mrs. K. Sunanda Reddy"),
("CSE_AI_ML","II","II","C","Database Management System","Mrs. Rajee Josan"),
("CSE_AI_ML","II","II","C","Introduction to Artificial Intelligence","Mr. S. Manikandan"),
("CSE_AI_ML","II","II","C","Object Oriented programming through Java","Mrs. G. Soumya"),

# LABS (Faculty 1)
("CSE_AI_ML","II","II","C","Database Management System Lab","Mrs. Rajee Josan"),
("CSE_AI_ML","II","II","C","Java Programming Lab","Mrs. G. Soumya"),
("CSE_AI_ML","II","II","C","Real Time Research Project","Mrs. G. Soumya"),
("CSE_AI_ML","II","II","C","PROLOG/LISP/PYSWIP","Mr. S. Manikandan"),


# ------------------ III / II / A ------------------

("CSE_AI_ML","III","II","A","Knowledge Representation and Reasoning","Mrs. Anju Gopi"),
("CSE_AI_ML","III","II","A","Data Analytics","Mrs. Pragathi B"),
("CSE_AI_ML","III","II","A","Natural Language Processing","Mrs. E. Amruthavarshini"),
("CSE_AI_ML","III","II","A","Software Testing Methodologies","Mrs. D. Ramadevi"),
("CSE_AI_ML","III","II","A","Fundamentals of Internet of Things","Mr. Praneel Deva"),

("CSE_AI_ML","III","II","A","Natural Language Processing Lab","Mrs. E. Amruthavarshini"),
("CSE_AI_ML","III","II","A","Data Analytics Lab","Mrs. Pragathi B"),
("CSE_AI_ML","III","II","A","Industrial Oriented Mini Project","Mrs. E. Amruthavarshini"),


# ------------------ III / II / B ------------------

("CSE_AI_ML","III","II","B","Knowledge Representation and Reasoning","Mrs. Anju Gopi"),
("CSE_AI_ML","III","II","B","Data Analytics","Dr. K. Shanthilatha"),
("CSE_AI_ML","III","II","B","Natural Language Processing","Mr. K. Lokesh"),
("CSE_AI_ML","III","II","B","Software Testing Methodologies","Mrs. D. Ramadevi"),
("CSE_AI_ML","III","II","B","Fundamentals of Internet of Things","Mr. Praneel Deva"),

("CSE_AI_ML","III","II","B","Natural Language Processing Lab","Mrs. Thamburu S"),
("CSE_AI_ML","III","II","B","Data Analytics Lab","Mrs. D. Ramadevi"),
("CSE_AI_ML","III","II","B","Industrial Oriented Mini Project","Mrs. Anju Gopi"),


# ------------------ III / II / C ------------------

("CSE_AI_ML","III","II","C","Knowledge Representation and Reasoning","Mrs. Ch. Pravallika"),
("CSE_AI_ML","III","II","C","Data Analytics","Mrs. Pragathi B"),
("CSE_AI_ML","III","II","C","Natural Language Processing","Mrs. E. Amruthavarshini"),
("CSE_AI_ML","III","II","C","Software Testing Methodologies","Mrs. Thamburu S"),
("CSE_AI_ML","III","II","C","Fundamentals of Internet of Things","Mr. Praneel Deva"),

("CSE_AI_ML","III","II","C","Natural Language Processing Lab","Mrs. Ch. Pravallika"),
("CSE_AI_ML","III","II","C","Data Analytics Lab","Mrs. S. Minisha Reddy"),
("CSE_AI_ML","III","II","C","Industrial Oriented Mini Project","Mrs. Ch. Pravallika"),


# -------- IV / I / A --------
("CSE_AI_ML","IV","I","A","SOCIAL NETWORK ANALYSIS","Dr. Anantha Raman G R"),
("CSE_AI_ML","IV","I","A","CONVERSATIONAL AI","Mr. K. Lokesh"),
("CSE_AI_ML","IV","I","A","COMMUNICATION TECHNOLOGIES","Dr. Vamshi"),
("CSE_AI_ML","IV","I","A","PROJECT STAGE-II INCLUDING SEMINAR","Mr. K. Lokesh"),


# -------- IV / II / B --------
("CSE_AI_ML","IV","II","B","SOCIAL NETWORK ANALYSIS","Mr. M. Sakthivel"),
("CSE_AI_ML","IV","II","B","CONVERSATIONAL AI","Mr. S. Srikanth"),
("CSE_AI_ML","IV","II","B","COMMUNICATION TECHNOLOGIES","Dr. B. Raju"),
("CSE_AI_ML","IV","II","B","PROJECT STAGE-II INCLUDING SEMINAR","Mr. M. Sakthivel"),


# -------- IV / II / C --------
("CSE_AI_ML","IV","II","C","SOCIAL NETWORK ANALYSIS","Mrs. S. Mineesha"),
("CSE_AI_ML","IV","II","C","CONVERSATIONAL AI","Mr. S. Srikanth"),
("CSE_AI_ML","IV","II","C","COMMUNICATION TECHNOLOGIES","Dr. B. Raju"),
("CSE_AI_ML","IV","II","C","PROJECT STAGE-II INCLUDING SEMINAR","Mr. M. Sakthivel"),

("CSD","III","II","A","Automata Theory and Compiler Design","Mrs.M.BHAGYALAXMI"),
("CSD","III","II","A","Machine Learning","Mr.V.THARMALINGAM"),
("CSD","III","II","A","Big Data Analytics","Dr.M.NARESH"),
("CSD","III","II","A","Software Testing Methodologies","Mrs.V.MOUNIKA"),
("CSD","III","II","A","Fundamentals of Internet of Things","Mrs.K.VIJAYABHARATHI"),
("CSD","III","II","A","Machine learning Lab","Mr.V.THARMALINGAM / Mrs.LIRINA P / Mrs.M.BHAGYALAXMI"),
("CSD","III","II","A","Big Data Analytics Lab","Mr.R.KAMALAKAR / Mr.R.HARISH KUMAR / Mr.K.VIJAYABHARATHI"),
("CSD","III","II","A","Software Testing Methodologies lab","Mrs.V.MOUNIKA / Mrs.NEELIMA / Mrs.M.NAGA SHARANYA"),
("CSD","III","II","A","UI design flutter","Mrs.M.BHAGYALAXMI / MR.SAJIN"),
("CSD","III","II","A","Environmental Science","Mrs.LIRINA P"),


("CSD","III","II","B","Automata Theory and Compiler Design","Dr.N.SATEESH"),
("CSD","III","II","B","Machine Learning","Mr.CH.KUMARASWAMY"),
("CSD","III","II","B","Big Data Analytics","Mr.R.HARISH KUMAR"),
("CSD","III","II","B","Software Testing Methodologies","Mr.M.P PRAVEEN KUMAR"),
("CSD","III","II","B","Fundamentals of Internet of Things","Mr.R.KAMALAKAR"),
("CSD","III","II","B","Machine learning Lab","Mr.CH.KUMARASWAMY / Mrs.SANDYA / Mr.AKASH DEY"),
("CSD","III","II","B","Big Data Analytics Lab","Mr.AKASH DEY / Mr.R.KAMALAKAR / Mr.M.SAILU"),
("CSD","III","II","B","Software Testing Methodologies lab","Mr.M.P.P PRAVEEN KUMAR / Mr.A.PRASHANTH / Mr.SAJIN R NAIR"),
("CSD","III","II","B","UI design flutter","Mrs.E.WILVATHI / Mr.CH.KUMARASWAMY"),
("CSD","III","II","B","Environmental Science","Mrs.LIRINA P"),


("CSD","III","II","C","Automata Theory and Compiler Design","Mrs.M.BHAGYALAXMI"),
("CSD","III","II","C","Machine Learning","Dr.J.BRITTO"),
("CSD","III","II","C","Big Data Analytics","Mr.HARISH KUMAR"),
("CSD","III","II","C","Software Testing Methodologies","Mrs.NEELIMA"),
("CSD","III","II","C","Fundamentals of Internet of Things","Mrs.VIJAYABHARATHI"),
("CSD","III","II","C","Machine learning Lab","Mrs.SANDYA / Mr.CH.KUMARASWAMY / Mrs.NEELIMA"),
("CSD","III","II","C","Big Data Analytics Lab","Mr.HARISHKUMAR / Mrs.VIJAYABHARATHI / Mr.RAMESH"),
("CSD","III","II","C","Software Testing Methodologies lab","Mrs.NEELIMA / Mrs.V.MOUNIKA / Mr.PRASHANTH"),
("CSD","III","II","C","UI design flutter","Mrs.KURRI RAJANI / Mrs.SANDHYA"),
("CSD","III","II","C","Environmental Science","Mrs.LIRINA P"),


("CSD","III","II","D","Automata Theory and Compiler Design","Dr.N.SATEESH"),
("CSD","III","II","D","Machine Learning","Mrs.LIRINA P"),
("CSD","III","II","D","Big Data Analytics","Dr.NARESH"),
("CSD","III","II","D","Software Testing Methodologies","Mr.PRASHANTH"),
("CSD","III","II","D","Fundamentals of Internet of Things","Mr.PANDU"),
("CSD","III","II","D","Machine learning Lab","Mrs.LIRINA P / Mr.THARMALINGAM / Mrs.BHAGYALAXMI"),
("CSD","III","II","D","Big Data Analytics Lab","Mr.R.KAMALAKAR / Mr.PANDU / Mrs.V.MOUNIKA"),
("CSD","III","II","D","Software Testing Methodologies lab","Mr.PRASHANTH / Mr.PRAVEEN KUMAR / Mrs.V.MOUNIKA"),
("CSD","III","II","D","UI design flutter","Mr.M.RADHAKRISHNAN / Mrs.LIRINA P"),
("CSD","III","II","D","Environmental Science","Mrs.LIRINA P"),

("CSD","IV","II","A","Organizational Behaviour","Mrs.V.MOUNIKA"),
("CSD","IV","II","A","Block Chain Technology","Mrs.NAGA SHARANYA"),
("CSD","IV","II","A","Charging Infrastructure for Electrical Vehicles","Mrs.E.WILVATHI"),


("CSD","IV","II","B","Organizational Behaviour","Mr.DEY AKASH"),
("CSD","IV","II","B","Block Chain Technology","Mr.V.RAMESH"),
("CSD","IV","II","B","Charging Infrastructure for Electrical Vehicles","Dr.SANDHYA RANI"),

("CSD","IV","II","C","Organizational Behaviour","Mr.DEY AKASH"),
("CSD","IV","II","C","Block Chain Technology","Mr.R.RAVI"),
("CSD","IV","II","C","Charging Infrastructure for Electrical Vehicles","Dr.SANDHYA RANI"),

("AI_DS","IV","II","A","Web Security","Mrs.NAGA SHARANYA"),
("AI_DS","IV","II","A","Semantic Web","Mr.PRASHANTH"),
("AI_DS","IV","II","A","Charging Infrastructure for Electrical Vehicles","Mrs.E.WILVATHI"),

("CSD","II","II","A","Discrete Mathematics","Dr.Manjula"),
("CSD","II","II","A","Business Economics & Financial Analysis","Mr.G.Niranjan Kumar"),
("CSD","II","II","A","Operating Systems","Mrs.K.Shravanthi"),
("CSD","II","II","A","Database Management Systems","Mr.Sailu"),
("CSD","II","II","A","Software Engineering","Mr.R.Ravi"),
("CSD","II","II","A","Operating Systems Lab","Mrs.K.Shravanthi / Mr.R.Ravi / Mrs.Kayal Vizhi"),
("CSD","II","II","A","Database Management Systems Lab","Mr.Sailu / Mr.Hanok Trinity / Mrs.Lirina P"),
("CSD","II","II","A","Real-time Research Project","Mrs.Kayal Vizhi / Mr.Naga Sharanya / Mrs.G.Priyanka"),
("CSD","II","II","A","Node JS / React JS / Django","Mr.R.Ravi / Mrs.K.Shravanthi / Mrs.Neelima"),
("CSD","II","II","A","Constitution of India","Mr.Ravi"),


("CSD","II","II","C","Discrete Mathematics","Dr.Manjula"),
("CSD","II","II","C","Business Economics & Financial Analysis","Mr.G.Niranjan Kumar"),
("CSD","II","II","C","Operating Systems","Mr.Sajin.R.Nair"),
("CSD","II","II","C","Database Management Systems","Mrs.Kayal Vizhi"),
("CSD","II","II","C","Software Engineering","Mr.V.Ramesh"),
("CSD","II","II","C","Operating Systems Lab","Mr.Sajin.R.Nair / Mrs.E.Wilvathi / Mr.V.Tharmalingam"),
("CSD","II","II","C","Database Management Systems Lab","Mrs.Kayal Vizhi / Mrs.K.Rajani / Mrs.BhagyaLakshmi"),
("CSD","II","II","C","Real-time Research Project","Mr.V.Hanok Trinity / Mr.R.Ravi / Mr.Kamalakar"),
("CSD","II","II","C","Node JS / React JS / Django Lab","Mr.V.Ramesh / Mr.Rajesh / Mrs.V.Mounica"),
("CSD","II","II","C","Constitution of India","Mrs.V.Mounika"),


("CSD","II","II","B","Discrete Mathematics","Dr.Manjula"),
("CSD","II","II","B","Business Economics & Financial Analysis","Mr.G.Niranjan Kumar"),
("CSD","II","II","B","Operating Systems","Mr.M.Radhakrishnan"),
("CSD","II","II","B","Database Management Systems","Mrs.Kurri Rajani"),
("CSD","II","II","B","Software Engineering","Dr.E.Lingappa"),
("CSD","II","II","B","Operating Systems Lab","Mr.M.Radhakrishnan / Mr.Akash Dey / Mrs.VijayaBharathi"),
("CSD","II","II","B","Database Management Systems Lab","Mrs.Kurri Rajani / Mrs.Kayal Vizhi / Mrs.Lirina P"),
("CSD","II","II","B","Real-time Research Project","Mrs.E.Wilvathi / Mrs.NagaSharanya / Mr.Akash Dey"),
("CSD","II","II","B","Node JS / React JS / Django Lab","Mr.Ch.Rajesh / Mr.V.Ramesh / Mr.Sailu"),
("CSD","II","II","B","Constitution of India","Mrs.V.Mounika"),


("CSD","II","II","D","Discrete Mathematics","Dr.Manjula"),
("CSD","II","II","D","Business Economics & Financial Analysis","Mr.G.Niranjan Kumar"),
("CSD","II","II","D","Operating Systems","Mrs.G.Priyanka"),
("CSD","II","II","D","Database Management Systems","Mr.Hanok Trinity"),
("CSD","II","II","D","Software Engineering","Dr.E.Lingappa"),
("CSD","II","II","D","Operating Systems Lab","Mr.V.Tharmalingam / Mrs.E.Wilvathi / Mr.Kumaraswamy"),
("CSD","II","II","D","Database Management Systems Lab","Mr.Hanok Trinity / Mr.Sailu / Mr.Ravi"),
("CSD","II","II","D","Real-time Research Project","Mrs.Naga Sharanya / Mrs.Neelima"),
("CSD","II","II","D","Node JS / React JS / Django","Mr.Ch.Rajesh / Mr.M.Praveen Kumar / Mr.V.Ramesh"),
("CSD","II","II","D","Constitution of India","Mr.V.Ramesh"),

("ECE","IV","II","A","5G and beyond Communications","Mrs.G.Rizwani"),
("ECE","IV","II","A","Wireless Sensor Networks","Dr.P.Sampath Kumar"),
("ECE","IV","II","A","Measuring Instruments","Mr.P.Bala Suresh Reddy"),
("ECE","IV","II","A","Project Stage – II including Seminar","Dr.P.Sampath Kumar"),

("ECE","IV","II","B","5G and beyond Communications","Mrs.G.Rizwani"),
("ECE","IV","II","B","Wireless Sensor Networks","Mr.B.Rama Krishna"),
("ECE","IV","II","B","Measuring Instruments","Mr.P.Bala Suresh Reddy"),
("ECE","IV","II","B","Project Stage – II including Seminar","Dr.P.Sampath Kumar"),

("ECE","II","II","A","Probability Theory and Stochastic Processes","Mr.G.Malyadri"),
("ECE","II","II","A","Electromagnetic Fields and Transmission Lines","Mrs.K.Maheswari"),
("ECE","II","II","A","Analog and Digital Communications","Ms.Neha Sultana"),
("ECE","II","II","A","Linear and Digital IC Applications","Mrs.N.Divya Jyothi"),
("ECE","II","II","A","Electronic Circuit Analysis","Mr.K.Harish Gandhi"),
("ECE","II","II","A","Analog and Digital Communications Laboratory","Ms.Neha Sultana / Mrs.K.Maheswari"),
("ECE","II","II","A","Linear and Digital IC Applications Laboratory","Mrs.N.Divya Jyothi / Mrs.G.Rizwani"),
("ECE","II","II","A","Electronic Circuit Analysis Laboratory","Mr.G.Malyadri / Mr.K.Harish Gandhi"),
("ECE","II","II","A","Real Time Project/ Field Based Project","Mr.B.Rama Krishna"),

("ECE","II","II","B","Probability Theory and Stochastic Processes","Mr.G.Malyadri"),
("ECE","II","II","B","Electromagnetic Fields and Transmission Lines","Mrs.K.Maheswari"),
("ECE","II","II","B","Analog and Digital Communications","Ms.Neha Sultana"),
("ECE","II","II","B","Linear and Digital IC Applications","Mrs.N.Divya Jyothi"),
("ECE","II","II","B","Electronic Circuit Analysis","Mr.K.Harish Gandhi"),
("ECE","II","II","B","Analog and Digital Communications Laboratory","Mrs.K.Maheswari / Ms.Neha Sultana"),
("ECE","II","II","B","Linear and Digital IC Applications Laboratory","Mrs.G.Rizwani / Mrs.N.Divya Jyothi"),
("ECE","II","II","B","Electronic Circuit Analysis Laboratory","Mr.K.Harish Gandhi / Mr.G.Malyadri"),
("ECE","II","II","B","Real Time Project/ Field Based Project","Mr.B.Rama Krishna"),

("ECE","III","II","A","Antennas and Wave Propagation","Dr.B.Madhavi"),
("ECE","III","II","A","Digital Signal Processing","Mr.I.Obulesu"),
("ECE","III","II","A","CMOS VLSI Design","Mr.B.Nihar"),
("ECE","III","II","A","Embedded System Design","Mrs.S.Rajeswari"),
("ECE","III","II","A","Fundamentals of AI","Mr.SK.Sohel Pasha"),
("ECE","III","II","A","Digital Signal Processing Laboratory","Mr.I.Obulesu / Mr.P.Balasuresh Reddy"),
("ECE","III","II","A","CMOS VLSI Design Laboratory","Mr.B.Nihar / Mr.Shaik Sohel Pasha"),
("ECE","III","II","A","Advanced Communication Laboratory","Dr.B.Madhavi / Mrs.S.Rajeswari"),
("ECE","III","II","A","Environmental Science","Mr.Anil Kumar"),
("ECE","III","II","A","Industry Oriented Mini Project/ Internship","Mr.SK.Sohel Pasha"),

("ECE","III","II","B","Antennas and Wave Propagation","Dr.B.Madhavi"),
("ECE","III","II","B","Digital Signal Processing","Mr.I.Obulesu"),
("ECE","III","II","B","CMOS VLSI Design","Mr.B.Nihar"),
("ECE","III","II","B","Embedded System Design","Mr.M.Shiva Kumar"),
("ECE","III","II","B","Fundamentals of AI","Mr.SK.Sohel Pasha"),
("ECE","III","II","B","Digital Signal Processing Laboratory","Mr.I.Obulesu / Mr.P.Balasuresh Reddy"),
("ECE","III","II","B","CMOS VLSI Design Laboratory","Mr.B.Nihar / Mr.M.Shiva Kumar"),
("ECE","III","II","B","Advanced Communication Laboratory","Dr.B.Madhavi / Mrs.S.Rajeswari"),
("ECE","III","II","B","Environmental Science","Mr.Anil Kumar"),
("ECE","III","II","B","Industry Oriented Mini Project/ Internship","Mr.M.Shiva Kumar"),


# ------------------ CSE III-II ------------------

# -------- SECTION A --------
("CSE","III","II","A","Machine Learning","Mr. K. Krishna"),
("CSE","III","II","A","Formal Languages and Automata Theory","Dr. L. V. Ramesh / Mrs. Sashwati Acharya"),
("CSE","III","II","A","Artificial Intelligence","Mr. B. Vinod"),
("CSE","III","II","A","Mobile Application Development","Mr. Lakshmi Reddy"),
("CSE","III","II","A","Fundamentals of Internet of Things","Mr. Ch. Sagar"),
("CSE","III","II","A","Machine Learning Lab","Mr. K. Krishna / Mrs. E. Venkateswaramma"),
("CSE","III","II","A","Artificial Intelligence Lab","Mr. B. Vinod / Mrs. S. Naveena"),
("CSE","III","II","A","Mobile Application Development Lab","Mr. Lakshmi Reddy / Mr. A. Ramakrishna"),

# -------- SECTION B --------
("CSE","III","II","B","Machine Learning","Mrs. Pushpa Joshi"),
("CSE","III","II","B","Formal Languages and Automata Theory","Mr. B. Srinivas"),
("CSE","III","II","B","Artificial Intelligence","Mr. V. Ravinder"),
("CSE","III","II","B","Mobile Application Development","Mr. B. ShivaKarthik"),
("CSE","III","II","B","Fundamentals of Internet of Things","Mr. K. Anil Kumar"),
("CSE","III","II","B","Machine Learning Lab","Mrs. Pushpa Joshi / Mr. B. Srinivas"),
("CSE","III","II","B","Artificial Intelligence Lab","Mr. V. Ravinder / Ms. P. Veena"),
("CSE","III","II","B","Mobile Application Development Lab","Mr. B. ShivaKarthik / Mr. A. Ramakrishna"),

# -------- SECTION C --------
("CSE","III","II","C","Machine Learning","Mr. K. Koteswara Rao"),
("CSE","III","II","C","Formal Languages and Automata Theory","Mrs. S. Naveena"),
("CSE","III","II","C","Artificial Intelligence","Mr. Y. Shiva Rao"),
("CSE","III","II","C","Mobile Application Development","Mrs. L. Sunitha"),
("CSE","III","II","C","Fundamentals of Internet of Things","Ms. Veena"),
("CSE","III","II","C","Machine Learning Lab","Mr. K. Koteswara Rao / Mr. Ch. Sagar"),
("CSE","III","II","C","Artificial Intelligence Lab","Mr. Y. Shiva Rao / Ms. P. Veena"),
("CSE","III","II","C","Mobile Application Development Lab","Mrs. L. Sunitha / Mr. A. Ramakrishna"),

# -------- SECTION D --------
("CSE","III","II","D","Machine Learning","Mrs. Venkateswaramma"),
("CSE","III","II","D","Formal Languages and Automata Theory","Dr. L. V. Ramesh / Mrs. Sashwati Acharya"),
("CSE","III","II","D","Artificial Intelligence","Mr. B. Vinod"),
("CSE","III","II","D","Mobile Application Development","Mr. Lakshmi Reddy"),
("CSE","III","II","D","Fundamentals of Internet of Things","Mr. Sagar"),
("CSE","III","II","D","Machine Learning Lab","Mrs. Venkateswaramma / Mr. B. Srinivas"),
("CSE","III","II","D","Artificial Intelligence Lab","Mr. B. Vinod / Mrs. J. Ravali"),
("CSE","III","II","D","Mobile Application Development Lab","Mr. Lakshmi Reddy / Mr. A. Ramakrishna"),

# -------- SECTION E --------
("CSE","III","II","E","Machine Learning","Mr. N. Balaraman"),
("CSE","III","II","E","Formal Languages and Automata Theory","Mr. B. Srinivas"),
("CSE","III","II","E","Artificial Intelligence","Mr. V. Ravinder"),
("CSE","III","II","E","Mobile Application Development","Mr. B. ShivaKarthik"),
("CSE","III","II","E","Fundamentals of Internet of Things","Mr. K. Anil Kumar"),
("CSE","III","II","E","Machine Learning Lab","Mr. N. Balaraman / Mr. Ch. Sagar"),
("CSE","III","II","E","Artificial Intelligence Lab","Mr. V. Ravinder / Mrs. S. Naveena"),
("CSE","III","II","E","Mobile Application Development Lab","Mr. B. ShivaKarthik / Mr. A. Ramakrishna"),

# -------- SECTION F --------
("CSE","III","II","F","Machine Learning","Mr. K. Koteswara Rao"),
("CSE","III","II","F","Formal Languages and Automata Theory","Mrs. S. Naveena"),
("CSE","III","II","F","Artificial Intelligence","Mrs. J. Ravali"),
("CSE","III","II","F","Mobile Application Development","Mrs. L. Sunitha"),
("CSE","III","II","F","Fundamentals of Internet of Things","Ms. Veena"),
("CSE","III","II","F","Machine Learning Lab","Mr. K. Koteswara Rao / Mr. Ch. Sagar"),
("CSE","III","II","F","Artificial Intelligence Lab","Mrs. J. Ravali / Mr. Y. Shiva Rao"),
("CSE","III","II","F","Mobile Application Development Lab","Mrs. L. Sunitha / Mrs. J. Ravali"),

("CSE","II","II","A","Discrete Mathematics","Dr. S. NAGESHWAR RAO"),
("CSE","II","II","A","Business Economics&Financial Analysis","Mr. CH. RAMESH"),
("CSE","II","II","A","Operating Systems","Mrs. SK. SABHA"),
("CSE","II","II","A","Database Management Systems","Mr. B. RAJESH"),
("CSE","II","II","A","Software Engineering","Mrs. V. SWETHA"),
("CSE","II","II","A","Operating Systems Lab","Mrs. SK. SABHA / Mr. CH. RAMBABU"),
("CSE","II","II","A","Database Management Systems Lab","Mr. B. RAJESH / Mr. CH. RAMBABU"),
("CSE","II","II","A","Node JS Lab","Mrs. V. SWETHA / Mr. CH. RAMBABU"),


("CSE","II","II","B","Discrete Mathematics","Mr.M. ANAND"),
("CSE","II","II","B","Business Economics&Financial Analysis","Dr.G.Sri Krishna"),
("CSE","II","II","B","Operating Systems","Mr. B. VENKATESH"),
("CSE","II","II","B","Database Management Systems","Mr. Y. RAMKUMAR"),
("CSE","II","II","B","Software Engineering","Mrs. M. MRUDULA"),
("CSE","II","II","B","Operating Systems Lab","Mr. B. VENKATESH / Mr. CH. RAMBABU"),
("CSE","II","II","B","Database Management Systems Lab","Mr. Y. RAMKUMAR / Mr. B. VENKATESH"),
("CSE","II","II","B","Node JS Lab","Mrs. M. MRUDULA / Mr. CH. RAMBABU"),


("CSE","II","II","C","Discrete Mathematics","Mr.M. ANAND"),
("CSE","II","II","C","Business Economics&Financial Analysis","Dr.G.Sri Krishna"),
("CSE","II","II","C","Operating Systems","Dr. G. SRAVANTHI"),
("CSE","II","II","C","Database Management Systems","Mrs. C. VARALAKSHMI"),
("CSE","II","II","C","Software Engineering","Mrs. M. SRAVANTHI"),
("CSE","II","II","C","Operating Systems Lab","Dr. G. SRAVANTHI / Mr. B. VENKATESH"),
("CSE","II","II","C","Database Management Systems Lab","Mrs. C. VARALAKSHMI / Mr. B. VENKATESH"),
("CSE","II","II","C","Node JS Lab","Mrs. M. SRAVANTHI / Dr. G. SRAVANTHI"),


("CSE","II","II","D","Discrete Mathematics","Dr. S. NAGESHWAR RAO"),
("CSE","II","II","D","Business Economics&Financial Analysis","Mr. CH. RAMESH"),
("CSE","II","II","D","Operating Systems","Mrs. SK. SABHA"),
("CSE","II","II","D","Database Management Systems","Mr. B. RAJESH"),
("CSE","II","II","D","Software Engineering","Mrs. V. SWETHA"),
("CSE","II","II","D","Operating Systems Lab","Mrs. SK. SABHA / Mrs. M. VAMSI PRIYA"),
("CSE","II","II","D","Database Management Systems Lab","Mr. B. RAJESH / Mrs. M. VAMSI PRIYA"),
("CSE","II","II","D","Node JS Lab","Mrs. V. SWETHA / Mr. B. RAJESH"),



("CSE","II","II","E","Discrete Mathematics","Mr.M. ANAND"),
("CSE","II","II","E","Business Economics&Financial Analysis","Dr.G.Sri Krishna"),
("CSE","II","II","E","Operating Systems","Dr. K. ARCHANA"),
("CSE","II","II","E","Database Management Systems","Mr. Y. RAMKUMAR"),
("CSE","II","II","E","Software Engineering","Mrs. M. MRUDULA"),
("CSE","II","II","E","Operating Systems Lab","Dr. K. ARCHANA / Mr. CH. RAMBABU"),
("CSE","II","II","E","Database Management Systems Lab","Mr. Y. RAMKUMAR / Mr. CH. RAMBABU"),
("CSE","II","II","E","Node JS Lab","Mrs. M. MRUDULA / Mrs. M. VAMSI PRIYA"),


("CSE","II","II","F","Discrete Mathematics","Mr.M. ANAND"),
("CSE","II","II","F","Business Economics&Financial Analysis","Mr. CH. RAMESH"),
("CSE","II","II","F","Operating Systems","Mrs. M. VAMSI PRIYA"),
("CSE","II","II","F","Database Management Systems","Mr. B. MURALIKRISHNA"),
("CSE","II","II","F","Software Engineering","Mrs. M. SRAVANTHI"),
("CSE","II","II","F","Operating Systems Lab","Mrs. M. VAMSI PRIYA / Mrs. C. VARALAKSHMI"),
("CSE","II","II","F","Database Management Systems Lab","Mrs. C. VARALAKSHMI / Mr. B. VENKATESH"),
("CSE","II","II","F","Node JS Lab","Mrs. M. SRAVANTHI / Mrs. V. SWETHA"),



("CSE","IV","II","A","ORGANIZATIONAL BEHAVIOUR","Ms. SUFIA ENAYAT"),
("CSE","IV","II","A","HUMAN COMPUTER INTERACTION","Dr. MANJUNATH GADIPARTHI"),
("CSE","IV","II","A","CHAT BOT","Dr. MARAM ASHOK"),


("CSE","IV","II","B","ORGANIZATIONAL BEHAVIOUR","Dr. G.SRAVANTHI"),
("CSE","IV","II","B","HUMAN COMPUTER INTERACTION","Mrs. PUSHPA JOSHI"),
("CSE","IV","II","B","CHAT BOT","Mrs. M. VAMSIPRIYA"),


("CSE","IV","II","C","ORGANIZATIONAL BEHAVIOUR","Dr. G.SRAVANTHI"),
("CSE","IV","II","C","HUMAN COMPUTER INTERACTION","Mrs. PUSHPA JOSHI"),
("CSE","IV","II","C","CHAT BOT","Mrs. M. VAMSIPRIYA"),


("CSE","IV","II","D","ORGANIZATIONAL BEHAVIOUR","Ms. SUFIA ENAYAT"),
("CSE","IV","II","D","HUMAN COMPUTER INTERACTION","Dr. MANJUNATH GADIPARTHI"),
("CSE","IV","II","D","CHAT BOT","Dr. MARAM ASHOK"),
]

cur.executemany("""
INSERT INTO subjects
(branch, year, semester, section, subject_name, faculty_name)
VALUES (%s,%s,%s,%s,%s,%s)
""", subjects_data)

print("✅ subjects inserted")

con.commit()
con.close()

print("🎉 DATABASE PERFECTLY MATCHED WITH FLASK APP!")
