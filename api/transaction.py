from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import MySQLdb
from config import DB_CONFIG

transaction_bp = Blueprint("transaction", __name__, template_folder="../templates")

def get_db():
    return MySQLdb.connect(**DB_CONFIG)

@transaction_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM users WHERE id=%s", (session["user_id"],))
    balance = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return render_template("dashboard.html", balance=balance)

@transaction_bp.route("/deposit", methods=["POST"])
def deposit():
    amount = float(request.form["amount"])
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE users SET balance = balance + %s WHERE id=%s", (amount, session["user_id"]))
    cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, 'deposit', %s)", (session["user_id"], amount))
    db.commit()
    cursor.close()
    db.close()
    flash("Deposit successful")
    return redirect(url_for("transaction.dashboard"))

@transaction_bp.route("/withdraw", methods=["POST"])
def withdraw():
    amount = float(request.form["amount"])
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT balance FROM users WHERE id=%s", (session["user_id"],))
    balance = cursor.fetchone()[0]
    if balance >= amount:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE id=%s", (amount, session["user_id"]))
        cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, 'withdraw', %s)", (session["user_id"], amount))
        db.commit()
        flash("Withdrawal successful")
    else:
        flash("Insufficient funds")
    cursor.close()
    db.close()
    return redirect(url_for("transaction.dashboard"))

@transaction_bp.route("/history")
def history():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT type, amount, created_at FROM transactions WHERE user_id=%s ORDER BY created_at DESC", (session["user_id"],))
    transactions = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("transactions.html", transactions=transactions)
