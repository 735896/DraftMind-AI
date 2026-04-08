from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)


def generate_draft(topic, word_limit):
    prompt = f"""
You are an ethical academic assistant.

Rules:
- Do NOT generate fully polished final answers
- Encourage student edits
- Add placeholders
- Keep language simple
- Add reference suggestions

Task:
Generate an assignment draft on: {topic}
Word limit: {word_limit}

Format:
Title
Introduction
Body (with headings)
Conclusion
References
"""

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            params={"key": os.getenv("GOOGLE_API_KEY")},
            json=data
        )

        result = response.json()

        # Handle API errors safely
        if "candidates" not in result:
            return "⚠️ Error: Unable to generate response. Check API key or quota."

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"⚠️ Server Error: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic")
        word_limit = request.form.get("word_limit")

        draft = generate_draft(topic, word_limit)
        return jsonify({"draft": draft})

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)