from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "mysecretkey"  # Needed for session handling

users = {}  # In-memory user store

# Common CSS style for all pages
base_style = """
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f6f8;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }
    .container {
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        width: 350px;
        text-align: center;
    }
    h2 {
        margin-bottom: 20px;
        color: #333;
    }
    input[type=text], input[type=password] {
        width: 100%;
        padding: 10px;
        margin: 8px 0;
        border: 1px solid #ccc;
        border-radius: 6px;
    }
    input[type=submit] {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-size: 16px;
    }
    input[type=submit]:hover {
        background-color: #45a049;
    }
    a {
        display: inline-block;
        margin-top: 15px;
        color: #007BFF;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
</style>
"""

register_page = base_style + """
<div class="container">
<h2>Register</h2>
<form method="POST">
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <input type="submit" value="Register">
</form>
<a href="/login">Already have an account? Login here</a>
</div>
"""

login_page = base_style + """
<div class="container">
<h2>Login</h2>
<form method="POST">
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <input type="submit" value="Login">
</form>
<a href="/register">Don't have an account? Register here</a>
</div>
"""

secure_page = base_style + """
<div class="container">
<h2>Welcome, {{ username }}! 🎉</h2>
<p>This is a secure page only visible to logged-in users.</p>
<a href="/logout">Logout</a>
</div>
"""

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "Username already exists! <a href='/register'>Try again</a>"
        users[username] = password
        return redirect(url_for("login"))
    return render_template_string(register_page)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("secure"))
        return "Invalid credentials! <a href='/login'>Try again</a>"
    return render_template_string(login_page)

@app.route("/secure")
def secure():
    if "username" in session:
        return render_template_string(secure_page, username=session["username"])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/")
def home():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
