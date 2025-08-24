from flask import Flask, render_template, redirect, url_for, session
from flask_session import Session
from api.auth import auth_bp
from api.transaction import transaction_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(transaction_bp, url_prefix="/transaction")

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("transaction.dashboard"))
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
