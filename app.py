import os
from flask import Flask, request, jsonify, send_from_directory, render_template_string
from werkzeug.utils import secure_filename
import smtplib

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

students = []

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Internship Portal</title>
    <style>
        body {
            font-family: Arial;
            background: linear-gradient(120deg, #4facfe, #00f2fe);
            color: #333;
            text-align: center;
            padding: 50px;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 12px;
            width: 400px;
            margin: auto;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
        }
        button {
            background: #4facfe;
            border: none;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background: #00c6ff;
        }
        #result {
            margin-top: 20px;
            color: green;
        }
    </style>
</head>
<body>

<div class="card">
    <h2>Internship Registration</h2>

    <form id="form">
        <input type="text" name="name" placeholder="Enter Name" required>
        <input type="email" name="email" placeholder="Enter Email" required>
        <input type="file" name="resume" required>
        <button type="submit">Submit</button>
    </form>

    <div id="result"></div>
</div>

<script>
document.getElementById("form").addEventListener("submit", async function(e) {
    e.preventDefault();

    let formData = new FormData(this);

    let res = await fetch("/register", {
        method: "POST",
        body: formData
    });

    let data = await res.json();

    if (data.success) {
        document.getElementById("result").innerHTML = `
            Registered Successfully! <br><br>
            <a href="${data.resume_url}" target="_blank">View Resume</a>
        `;
        document.getElementById("form").reset();
    } else {
        document.getElementById("result").innerHTML = "Error!";
    }
});
</script>

</body>
</html>
""")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
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

    return jsonify({
        "success": True,
        "resume_url": f"/resume/{filename}"
    })

# ---------------- ADMIN API ----------------
@app.route("/api/students")
def get_students():
    return jsonify(students)

# ---------------- RESUME VIEW ----------------
@app.route("/resume/<filename>")
def resume(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ---------------- EMAIL ----------------
def send_email(to_email, name):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
        server.starttls()
        server.login("vishwendraditya@gmail.com", "fqqqivsxivrzxwoq")

        message = f"Subject: Registered\n\nHello {name}, you are registered!"
        server.sendmail("vishwendraditya@gmail.com", to_email, message)
        server.quit()

    except Exception as e:
        print("Email failed:", e)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
