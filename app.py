from flask import Flask, render_template, request, session, redirect, url_for
import json
import os
import random

app = Flask(__name__)
# A secret key is required for Flask sessions to work.
# In a real-world app, you would use a more complex, randomly generated key.
app.secret_key = 'your_secret_key_here'

# Load quiz questions from the JSON file
def load_questions():
    try:
        with open(os.path.join(app.root_path, 'questions.json'), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

questions = load_questions()
random.shuffle(questions) # Shuffle questions to make the quiz dynamic

@app.route('/')
def index():
    # Clear the session when a new quiz starts
    session.clear()
    session['quiz_questions'] = questions
    session['score'] = 0
    session['current_question_index'] = 0
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # If the user is trying to access the quiz without starting from the index page, redirect them.
    if 'quiz_questions' not in session:
        return redirect(url_for('index'))

    # Check if the form was submitted (i.e., a POST request)
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        
        # Get the current question and its correct answer
        current_question_index = session['current_question_index']
        current_question_data = session['quiz_questions'][current_question_index]
        correct_answer = current_question_data['correct_answer']
        
        # Check if the user's answer is correct and update the score
        if user_answer == correct_answer:
            session['score'] += 1
        
        # Move to the next question
        session['current_question_index'] += 1
        
        # Check if the quiz is finished
        if session['current_question_index'] >= len(session['quiz_questions']):
            return redirect(url_for('results'))

    # Display the current question for GET requests or after a POST
    current_question_index = session['current_question_index']
    current_question_data = session['quiz_questions'][current_question_index]
    
    return render_template('quiz.html', 
                           question=current_question_data,
                           total_questions=len(session['quiz_questions']),
                           current_question_number=current_question_index + 1)

@app.route('/results')
def results():
    # If there is no quiz session data, redirect to the start page
    if 'quiz_questions' not in session:
        return redirect(url_for('index'))
    
    total_questions = len(session['quiz_questions'])
    score = session['score']
    
    # Clear the session data after the results are shown
    session.clear()
    
    return render_template('results.html', score=score, total_questions=total_questions)

if __name__ == '__main__':
    # Ensure the questions.json file exists for demonstration
    if not os.path.exists('questions.json'):
        # Create a sample questions.json file if it doesn't exist
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
            }
        ]
        with open('questions.json', 'w') as file:
            json.dump(sample_questions, file, indent=4)
            
    app.run(debug=True)
