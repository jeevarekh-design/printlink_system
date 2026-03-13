from flask import Flask, render_template, request, redirect, session
import os
import pymysql

app = Flask(__name__)
app.secret_key = "printlink_secret"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# MySQL Connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="root123",
    database="printlink"
)


# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")


# ---------------- STUDENT MENU ----------------
@app.route("/student")
def student_menu():
    return render_template("student_menu.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()

        sql = "INSERT INTO students(name,email,password) VALUES(%s,%s,%s)"
        cursor.execute(sql, (name, email, password))

        db.commit()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor = db.cursor()

        sql = "SELECT * FROM students WHERE email=%s AND password=%s"
        cursor.execute(sql, (email, password))

        user = cursor.fetchone()

        if user:
            session["student"] = user[1]
            return redirect("/dashboard")

    return render_template("login.html")


# ---------------- STUDENT DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "student" not in session:
        return redirect("/login")

    return render_template("student_dashboard.html", name=session["student"])


# ---------------- UPLOAD DOCUMENT ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "student" not in session:
        return redirect("/login")

    if request.method == "POST":

        file = request.files["document"]
        copies = request.form["copies"]
        print_type = request.form["print_type"]

        filename = file.filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        cursor = db.cursor()

        sql = """
        INSERT INTO orders(student_name,file_name,copies,print_type,status)
        VALUES(%s,%s,%s,%s,%s)
        """

        cursor.execute(
            sql,
            (session["student"], filename, copies, print_type, "Inbox")
        )

        db.commit()

        return redirect("/dashboard")

    return render_template("upload.html")


# ---------------- TRACK ORDERS ----------------
@app.route("/track")
def track():

    if "student" not in session:
        return redirect("/login")

    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM orders WHERE student_name=%s",
        (session["student"],)
    )

    orders = cursor.fetchall()

    return render_template("track_order.html", orders=orders)


# =================================================
# ADMIN SECTION
# =================================================

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = username
            return redirect("/admin/dashboard")

    return render_template("admin/login.html")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin/login")

    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM orders")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE status='Inbox'")
    inbox = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE status='Printing'")
    printing = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE status='Ready'")
    ready = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders WHERE status='Delivered'")
    delivered = cursor.fetchone()[0]

    return render_template(
        "admin/dashboard.html",
        total=total,
        inbox=inbox,
        printing=printing,
        ready=ready,
        delivered=delivered
    )


# ---------------- ADMIN INBOX ----------------
@app.route("/admin/inbox")
def admin_inbox():

    if "admin" not in session:
        return redirect("/admin/login")

    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders WHERE status='Inbox'")
    orders = cursor.fetchall()

    return render_template("admin/inbox.html", orders=orders)


# ---------------- ADMIN PRINTING ----------------
@app.route("/admin/printing")
def admin_printing():

    if "admin" not in session:
        return redirect("/admin/login")

    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders WHERE status='Printing'")
    orders = cursor.fetchall()

    return render_template("admin/printing.html", orders=orders)


# ---------------- ADMIN READY ----------------
@app.route("/admin/ready")
def admin_ready():

    if "admin" not in session:
        return redirect("/admin/login")

    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders WHERE status='Ready'")
    orders = cursor.fetchall()

    return render_template("admin/ready.html", orders=orders)


# ---------------- ADMIN DELIVERED ----------------
@app.route("/admin/delivered")
def admin_delivered():

    if "admin" not in session:
        return redirect("/admin/login")

    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders WHERE status='Delivered'")
    orders = cursor.fetchall()

    return render_template("admin/delivered.html", orders=orders)


# ---------------- UPDATE ORDER STATUS ----------------
@app.route("/update_status/<int:id>/<status>")
def update_status(id, status):

    if "admin" not in session:
        return redirect("/admin/login")

    cursor = db.cursor()

    sql = "UPDATE orders SET status=%s WHERE id=%s"
    cursor.execute(sql, (status, id))

    db.commit()

    return redirect("/admin/inbox")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("student", None)
    session.pop("admin", None)

    return redirect("/")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)