from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb
from config import DB_CONFIG

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

def get_db():
    return MySQLdb.connect(**DB_CONFIG)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            flash("Registration successful! Please login.")
            return redirect(url_for("auth.login"))
        except:
            flash("Username already exists!")
        finally:
            cursor.close()
            db.close()
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect(url_for("transaction.dashboard"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
