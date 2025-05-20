from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Maxbot Tertiary Backend is running."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    level = data.get("level", "Tertiary")
    program = data.get("program", "General")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are Maxbot, an educational assistant helping {level} students in {program}."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message["content"].strip()
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))