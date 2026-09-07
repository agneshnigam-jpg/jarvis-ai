import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={API_KEY}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message.strip():
        return jsonify({"reply": "Kuch toh likho!"})

    try:
        payload = {
            "contents": [{"parts": [{"text": user_message}]}]
        }
        res = requests.post(GEMINI_URL, json=payload, timeout=50)
        data = res.json()

        if "candidates" in data:
            reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": reply_text})
        else:
            print("API RESPONSE ISSUE:", data)
            return jsonify({"reply": "Thodi si dikkat aayi, dobara try karo."})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"reply": "Thodi si dikkat aayi, dobara try karo."})


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
