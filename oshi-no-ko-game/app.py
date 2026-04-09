from flask import Flask, render_template, request, session
import random
import os  # Needed for Render

app = Flask(__name__)
app.secret_key = "supersecretkey123"

characters = {
    "Ai": ["Idol", "Blonde hair", "Star eyes", "Charming but secretive"],
    "Aqua": ["Actor", "Blue hair", "Blue eyes", "Calm and revenge-driven"],
    "Ruby": ["Idol", "Blonde hair", "Pink eyes", "Cheerful and determined"],
    "Kana": ["Actress", "Red hair", "Red eyes", "Tsundere and talented"],
    "Akane": ["Actress", "Dark blue hair", "Blue eyes", "Observant and analytical"],
    "Mem-Cho": ["Streamer", "Blonde hair", "Pink eyes", "Energetic and playful"],
    "Gorou": ["Doctor", "Black hair", "Dark eyes", "Kind and dedicated"],
    "Sarina": ["Patient", "Light hair", "Bright eyes", "Hopeful and kind"],
    "Ichigo": ["Manager", "Blonde hair", "Dark eyes", "Strict but caring"],
    "Miyako": ["Manager", "Brown hair", "Dark eyes", "Supportive and practical"],
    "Tsukuyomi": ["Creepy-looking child", "White hair", "Brown eyes", "Mischevious"]
}

def start_new_game():
    character = random.choice(list(characters.keys()))
    session["character"] = character
    session["hints"] = characters[character]
    session["hint_index"] = 0
    session["attempts"] = 0

@app.route("/", methods=["GET", "POST"])
def home():
    if "character" not in session:
        start_new_game()

    message = ""
    hint = ""

    if request.method == "POST":
        guess = request.form.get("guess", "").strip()
        session["attempts"] += 1

        if guess.lower() == session["character"].lower():
            message = f"🎉 Correct! It was {session['character']} in {session['attempts']} tries!"
            session.clear()
        else:
            message = "❌ Wrong!"
            if session["hint_index"] < len(session["hints"]):
                hint = session["hints"][session["hint_index"]]
                session["hint_index"] += 1
            else:
                message = f"💀 Out of hints! It was {session['character']}"
                session.clear()

    return render_template("index.html", message=message, hint=hint)

# RENDER-READY: use PORT from environment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides the PORT
    app.run(host="0.0.0.0", port=port)