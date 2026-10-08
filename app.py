import os
from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chat_history = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"answer": "Please enter a question."})

    chat_history.append({
        "role": "user",
        "text": question
    })

    conversation = """
You are an AI College Assistant.

Your job is to help students with questions about colleges, universities,
courses, admissions, eligibility, fees, scholarships, campuses, entrance
exams, placements, and student life.

Answer clearly, accurately, and concisely.

You can answer questions about ANY college or university the student asks about.

Use the previous conversation to understand follow-up questions, but do not
mention the conversation history or say phrases such as "based on our previous
conversation", "as you mentioned earlier", or "as discussed above" unless the
student specifically asks about the conversation.

If the question is unrelated to colleges or education, politely explain that
you are designed to help with college and education-related questions.

Conversation so far:
"""

    for message in chat_history:
        conversation += f"\n{message['role']}: {message['text']}"

    conversation += "\n\nAI College Assistant:"

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=conversation
        )

        answer = response.text

        chat_history.append({
            "role": "assistant",
            "text": answer
        })

        return jsonify({"answer": answer})

    except Exception:
        return jsonify({
            "answer": "Sorry, I couldn't process your question right now. Please try again."
        })


if __name__ == "__main__":
    app.run(debug=True)