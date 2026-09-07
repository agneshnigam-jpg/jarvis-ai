import os
from flask import Flask, request, jsonify, render_template
from google import genai

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message.strip():
        return jsonify({"reply": "Kuch toh likho!"})

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=user_message
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"reply": "Thodi si dikkat aayi, dobara try karo."}), 200


@app.route("/health")
def health():
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
