from flask import Flask, jsonify, redirect, render_template, request, url_for

from webapp.db import is_common_password, log_account_creation
from webapp.password_policy import validate_password

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


@app.after_request
def secure_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; form-action 'self'; frame-ancestors 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/")
@app.get("/create-account")
def home():
    return render_template("home.html", errors=[], username="")


@app.post("/create-account")
def create_account():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    errors = []
    if not username:
        errors.append("Username is required.")
    elif len(username) > 100:
        errors.append("Username must not exceed 100 characters.")
    errors.extend(validate_password(password, is_common_password))

    if errors:
        return render_template("home.html", errors=errors, username=username), 400

    log_account_creation(username)
    return render_template("welcome.html", username=username, password=password)


@app.post("/api/password-check")
def password_check():
    password = (request.get_json(silent=True) or {}).get("password")
    errors = validate_password(password, is_common_password)
    return jsonify(valid=not errors, errors=errors)


@app.post("/logout")
def logout():
    return redirect(url_for("home"))


@app.get("/health")
def health():
    return jsonify(status="healthy")
