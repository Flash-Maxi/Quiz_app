from flask import Flask, render_template, request, session, redirect, url_for
import json
import os
import random
from pathlib import Path

app = Flask(__name__)

# Use a strong, random secret key for security
# It will look for the SECRET_KEY environment variable set on Render
app.secret_key = os.environ.get("SECRET_KEY")

# Path to questions.json
QUESTIONS_FILE = Path(app.root_path) / "questions.json"

def load_questions():
    """Load quiz questions from JSON file, return empty list if not found."""
    if QUESTIONS_FILE.exists():
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

questions = load_questions()
random.shuffle(questions)  # Shuffle once at app start

@app.route("/")
def index():
    """Start a new quiz session."""
    session.clear()
    session["quiz_questions"] = questions
    session["score"] = 0
    session["current_question_index"] = 0
    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Main quiz route for displaying questions and handling answers."""
    if "quiz_questions" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        user_answer = request.form.get("answer")
        idx = session["current_question_index"]
        current_question = session["quiz_questions"][idx]
        correct_answer = current_question["correct_answer"]

        # Update score if correct
        if user_answer == correct_answer:
            session["score"] += 1

        session["current_question_index"] += 1

        # If quiz finished, redirect to results
        if session["current_question_index"] >= len(session["quiz_questions"]):
            return redirect(url_for("results"))

    # Show current question
    idx = session["current_question_index"]
    current_question = session["quiz_questions"][idx]
    return render_template(
        "quiz.html",
        question=current_question,
        total_questions=len(session["quiz_questions"]),
        current_question_number=idx + 1,
    )

@app.route("/results")
def results():
    """Display quiz results and clear session."""
    if "quiz_questions" not in session:
        return redirect(url_for("index"))

    total_questions = len(session["quiz_questions"])
    score = session["score"]

    session.clear()
    return render_template("results.html", score=score, total_questions=total_questions)

if __name__ == "__main__":
    # Auto-generate sample questions if not present for local dev
    if not QUESTIONS_FILE.exists():
        sample_questions = [
            {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "correct_answer": "Paris"},
            {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "correct_answer": "Mars"},
            {"question": "What is 7 + 8?", "options": ["12", "14", "15", "16"], "correct_answer": "15"},
            {"question": "Who wrote 'To Kill a Mockingbird'?", "options": ["Harper Lee", "Mark Twain", "J.K. Rowling", "Stephen King"], "correct_answer": "Harper Lee"},
            {"question": "What is the largest ocean on Earth?", "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"], "correct_answer": "Pacific Ocean"},
        ]
        with open(QUESTIONS_FILE, "w", encoding="utf-8") as file:
            json.dump(sample_questions, file, indent=4)

    app.run(debug=True)
