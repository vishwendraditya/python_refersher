import os
from flask import Flask, request, redirect, url_for, render_template_string, send_from_directory
from werkzeug.utils import secure_filename
import smtplib

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Temporary in-memory storage
students = []

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template_string("""
    <h2>Internship Portal</h2>
    <a href="/register">Register</a> | 
    <a href="/admin">Admin Dashboard</a>
    """)

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        file = request.files["resume"]

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        students.append({
            "name": name,
            "email": email,
            "resume": filename
        })

        send_email(email, name)

        return "Registered Successfully!"

    return render_template_string("""
    <h2>Register</h2>
    <form method="POST" enctype="multipart/form-data">
        Name: <input name="name"><br><br>
        Email: <input name="email"><br><br>
        Resume: <input type="file" name="resume"><br><br>
        <button type="submit">Submit</button>
    </form>
    """)

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    html = "<h2>Admin Dashboard</h2>"
    for s in students:
        html += f"""
        <p>
        Name: {s['name']} | Email: {s['email']} |
        <a href="/resume/{s['resume']}">View Resume</a>
        </p>
        """
    return html

# ---------------- RESUME VIEW ----------------
@app.route("/resume/<filename>")
def resume(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ---------------- EMAIL ----------------
def send_email(to_email, name):
    try:
        sender_email = "vishwendraditya@gmail.com"
        sender_password = "fqqqivsxivrzxwoq"

        message = f"Subject: Registration Successful\n\nHello {name}, you are registered!"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message)
        server.quit()
    except Exception as e:
        print("Email error:", e)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
