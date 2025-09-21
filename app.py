"""
Flask Quiz Application

A modern, interactive quiz application that provides an engaging way to test knowledge
through multiple-choice questions with session-based state management.

Author: Mystify7777
Version: 1.0.0
"""

import json
import logging
import os
import random
import secrets
from pathlib import Path
from typing import Dict, List, Optional

from flask import Flask, render_template, request, session, redirect, url_for, flash


class Config:
    """Application configuration class."""
    
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    QUESTIONS_FILE = "questions.json"
    MAX_QUESTIONS_PER_QUIZ = int(os.environ.get("MAX_QUESTIONS_PER_QUIZ", "10"))


class QuizService:
    """Service class to handle quiz-related business logic."""
    
    def __init__(self, questions_file: str):
        self.questions_file = Path(questions_file)
        self._questions_cache = None
        self.logger = logging.getLogger(__name__)
    
    def load_questions(self) -> List[Dict]:
        """
        Load quiz questions from JSON file with error handling.
        
        Returns:
            List of question dictionaries or empty list if file not found/invalid
        """
        if self._questions_cache is not None:
            return self._questions_cache
            
        try:
            if self.questions_file.exists():
                with open(self.questions_file, "r", encoding="utf-8") as file:
                    questions = json.load(file)
                    
                # Validate question format
                validated_questions = []
                for i, question in enumerate(questions):
                    if self._validate_question(question):
                        validated_questions.append(question)
                    else:
                        self.logger.warning(f"Invalid question format at index {i}: {question}")
                
                self._questions_cache = validated_questions
                self.logger.info(f"Loaded {len(validated_questions)} valid questions")
                return validated_questions
            else:
                self.logger.warning(f"Questions file not found: {self.questions_file}")
                return []
                
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"Error loading questions: {e}")
            return []
    
    def _validate_question(self, question: Dict) -> bool:
        """
        Validate question format.
        
        Args:
            question: Question dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        required_keys = ["question", "options", "correct_answer"]
        
        # Check required keys exist
        if not all(key in question for key in required_keys):
            return False
            
        # Check question is not empty
        if not question["question"].strip():
            return False
            
        # Check options is a list with at least 2 options
        if not isinstance(question["options"], list) or len(question["options"]) < 2:
            return False
            
        # Check correct answer is in options
        if question["correct_answer"] not in question["options"]:
            return False
            
        return True
    
    def get_shuffled_questions(self, max_questions: Optional[int] = None) -> List[Dict]:
        """
        Get shuffled questions for a new quiz session.
        
        Args:
            max_questions: Maximum number of questions to return
            
        Returns:
            List of shuffled questions
        """
        questions = self.load_questions().copy()
        random.shuffle(questions)
        
        if max_questions and len(questions) > max_questions:
            questions = questions[:max_questions]
            
        return questions
    
    def create_sample_questions(self) -> None:
        """Create sample questions file for development."""
        sample_questions = [
            {
                "question": "What is the capital of France?",
                "options": ["Berlin", "Madrid", "Paris", "Rome"],
                "correct_answer": "Paris"
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Earth", "Mars", "Jupiter", "Venus"],
                "correct_answer": "Mars"
            },
            {
                "question": "What is 7 + 8?",
                "options": ["12", "14", "15", "16"],
                "correct_answer": "15"
            },
            {
                "question": "Who wrote 'To Kill a Mockingbird'?",
                "options": ["Harper Lee", "Mark Twain", "J.K. Rowling", "Stephen King"],
                "correct_answer": "Harper Lee"
            },
            {
                "question": "What is the largest ocean on Earth?",
                "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
                "correct_answer": "Pacific Ocean"
            },
            {
                "question": "What is the chemical symbol for gold?",
                "options": ["Go", "Gd", "Au", "Ag"],
                "correct_answer": "Au"
            },
            {
                "question": "In which year did World War II end?",
                "options": ["1944", "1945", "1946", "1947"],
                "correct_answer": "1945"
            },
            {
                "question": "What is the smallest prime number?",
                "options": ["0", "1", "2", "3"],
                "correct_answer": "2"
            }
        ]
        
        try:
            with open(self.questions_file, "w", encoding="utf-8") as file:
                json.dump(sample_questions, file, indent=4)
            self.logger.info(f"Created sample questions file: {self.questions_file}")
        except IOError as e:
            self.logger.error(f"Error creating sample questions: {e}")


def create_app(config_class=Config) -> Flask:
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configure logging
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    
    # Initialize quiz service
    quiz_service = QuizService(app.config['QUESTIONS_FILE'])
    
    # Create sample questions if file doesn't exist (development only)
    if app.debug and not Path(app.config['QUESTIONS_FILE']).exists():
        quiz_service.create_sample_questions()
    
    return app, quiz_service


# Create Flask app instance
app, quiz_service = create_app()

# Route Handlers
@app.route("/")
def index():
    """
    Display the welcome page and initialize a new quiz session.
    
    Returns:
        Rendered index template
    """
    try:
        # Clear any existing session data
        session.clear()
        
        # Get fresh shuffled questions for this session
        questions = quiz_service.get_shuffled_questions(app.config['MAX_QUESTIONS_PER_QUIZ'])
        
        if not questions:
            flash("No questions available. Please contact the administrator.", "error")
            app.logger.warning("No questions available for quiz")
        
        # Initialize session data
        session["quiz_questions"] = questions
        session["score"] = 0
        session["current_question_index"] = 0
        session["answers"] = []  # Track user answers for review
        
        return render_template("index.html", total_questions=len(questions))
        
    except Exception as e:
        app.logger.error(f"Error in index route: {e}")
        flash("An error occurred while starting the quiz. Please try again.", "error")
        return render_template("index.html", total_questions=0)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """
    Main quiz route for displaying questions and handling answers.
    
    Returns:
        Rendered quiz template or redirect to results
    """
    # Validate session state
    if not _is_valid_quiz_session():
        flash("Quiz session expired. Please start a new quiz.", "warning")
        return redirect(url_for("index"))
    
    try:
        if request.method == "POST":
            return _handle_quiz_answer()
        else:
            return _display_current_question()
            
    except Exception as e:
        app.logger.error(f"Error in quiz route: {e}")
        flash("An error occurred during the quiz. Please try again.", "error")
        return redirect(url_for("index"))


@app.route("/results")
def results():
    """
    Display quiz results and provide option to start new quiz.
    
    Returns:
        Rendered results template
    """
    # Validate session state
    if not _is_valid_quiz_session():
        flash("No quiz results found. Please start a new quiz.", "warning")
        return redirect(url_for("index"))
    
    try:
        total_questions = len(session["quiz_questions"])
        score = session["score"]
        answers = session.get("answers", [])
        
        # Calculate percentage
        percentage = round((score / total_questions) * 100) if total_questions > 0 else 0
        
        # Determine performance message
        if percentage >= 80:
            performance_msg = "Excellent! Outstanding performance!"
            performance_class = "excellent"
        elif percentage >= 60:
            performance_msg = "Good job! Well done!"
            performance_class = "good"
        elif percentage >= 40:
            performance_msg = "Not bad! Room for improvement."
            performance_class = "average"
        else:
            performance_msg = "Keep practicing! You'll improve!"
            performance_class = "needs-improvement"
        
        # Prepare results data
        results_data = {
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "performance_msg": performance_msg,
            "performance_class": performance_class,
            "answers": answers
        }
        
        # Clear session after getting results
        session.clear()
        
        return render_template("results.html", **results_data)
        
    except Exception as e:
        app.logger.error(f"Error in results route: {e}")
        flash("An error occurred while displaying results.", "error")
        return redirect(url_for("index"))


# Helper Functions
def _is_valid_quiz_session() -> bool:
    """
    Check if the current session has valid quiz data.
    
    Returns:
        True if session is valid, False otherwise
    """
    required_keys = ["quiz_questions", "score", "current_question_index"]
    return all(key in session for key in required_keys)


def _handle_quiz_answer():
    """
    Process user's answer submission.
    
    Returns:
        Redirect to next question or results page
    """
    user_answer = request.form.get("answer")
    
    if not user_answer:
        flash("Please select an answer before proceeding.", "warning")
        return redirect(url_for("quiz"))
    
    idx = session["current_question_index"]
    current_question = session["quiz_questions"][idx]
    correct_answer = current_question["correct_answer"]
    
    # Record the answer
    is_correct = user_answer == correct_answer
    answer_record = {
        "question": current_question["question"],
        "user_answer": user_answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct,
        "options": current_question["options"]
    }
    
    if "answers" not in session:
        session["answers"] = []
    session["answers"].append(answer_record)
    
    # Update score if correct
    if is_correct:
        session["score"] += 1
    
    # Move to next question
    session["current_question_index"] += 1
    
    # Check if quiz is finished
    if session["current_question_index"] >= len(session["quiz_questions"]):
        return redirect(url_for("results"))
    
    return redirect(url_for("quiz"))


def _display_current_question():
    """
    Display the current question in the quiz.
    
    Returns:
        Rendered quiz template
    """
    idx = session["current_question_index"]
    
    # Validate question index
    if idx >= len(session["quiz_questions"]):
        return redirect(url_for("results"))
    
    current_question = session["quiz_questions"][idx]
    total_questions = len(session["quiz_questions"])
    
    # Calculate progress percentage
    progress_percentage = round((idx / total_questions) * 100)
    
    return render_template(
        "quiz.html",
        question=current_question,
        total_questions=total_questions,
        current_question_number=idx + 1,
        progress_percentage=progress_percentage
    )


# Error Handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template("error.html", 
                         error_code=404, 
                         error_message="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    app.logger.error(f"Internal server error: {error}")
    return render_template("error.html", 
                         error_code=500, 
                         error_message="Internal server error"), 500


if __name__ == "__main__":
    # Ensure we have a secret key in development
    if not app.config['SECRET_KEY']:
        app.logger.warning("No SECRET_KEY set. Using a temporary key for development.")
        app.config['SECRET_KEY'] = secrets.token_hex(32)
    
    # Run the application
    app.run(
        debug=app.config['DEBUG'],
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", 5000))
    )
