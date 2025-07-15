from flask import Flask, render_template, request, jsonify, session
import os
import json
import random
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Sample lessons data
LESSONS = {
    'beginner': [
        {
            'id': 1,
            'title': 'Basic Greetings',
            'phrases': [
                {'text': 'Hello, how are you?', 'difficulty': 'easy'},
                {'text': 'Good morning!', 'difficulty': 'easy'},
                {'text': 'Nice to meet you.', 'difficulty': 'easy'},
                {'text': 'How do you do?', 'difficulty': 'medium'},
            ]
        },
        {
            'id': 2,
            'title': 'Common Expressions',
            'phrases': [
                {'text': 'Thank you very much.', 'difficulty': 'easy'},
                {'text': 'You are welcome.', 'difficulty': 'easy'},
                {'text': 'Excuse me, please.', 'difficulty': 'medium'},
                {'text': 'I beg your pardon?', 'difficulty': 'medium'},
            ]
        }
    ],
    'intermediate': [
        {
            'id': 3,
            'title': 'Business English',
            'phrases': [
                {'text': 'I would like to schedule a meeting.', 'difficulty': 'medium'},
                {'text': 'Could you please send me the report?', 'difficulty': 'medium'},
                {'text': 'I appreciate your assistance.', 'difficulty': 'hard'},
                {'text': 'Let me get back to you on that.', 'difficulty': 'hard'},
            ]
        }
    ],
    'advanced': [
        {
            'id': 4,
            'title': 'Idiomatic Expressions',
            'phrases': [
                {'text': 'It\'s raining cats and dogs.', 'difficulty': 'hard'},
                {'text': 'Break a leg with your presentation!', 'difficulty': 'hard'},
                {'text': 'The ball is in your court now.', 'difficulty': 'hard'},
                {'text': 'Don\'t beat around the bush.', 'difficulty': 'hard'},
            ]
        }
    ]
}

# Initialize user progress
def init_user_progress():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    if 'progress' not in session:
        session['progress'] = {
            'completed_lessons': [],
            'pronunciation_scores': {},
            'total_score': 0,
            'streak_days': 0
        }

@app.route('/')
def index():
    init_user_progress()
    return render_template('index.html')

@app.route('/lessons')
def lessons():
    init_user_progress()
    return render_template('lessons.html', lessons=LESSONS)

@app.route('/lesson/<level>/<int:lesson_id>')
def lesson_detail(level, lesson_id):
    init_user_progress()
    
    # Find the specific lesson
    lesson = None
    for lesson_data in LESSONS.get(level, []):
        if lesson_data['id'] == lesson_id:
            lesson = lesson_data
            break
    
    if not lesson:
        return "Lesson not found", 404
    
    return render_template('lesson_detail.html', lesson=lesson, level=level)

@app.route('/practice')
def practice():
    init_user_progress()
    
    # Get a random phrase for practice
    all_phrases = []
    for level_lessons in LESSONS.values():
        for lesson in level_lessons:
            all_phrases.extend(lesson['phrases'])
    
    random_phrase = random.choice(all_phrases)
    return render_template('practice.html', phrase=random_phrase)

@app.route('/progress')
def progress():
    init_user_progress()
    user_progress = session.get('progress', {})
    return render_template('progress.html', progress=user_progress)

@app.route('/api/submit_pronunciation', methods=['POST'])
def submit_pronunciation():
    data = request.get_json()
    phrase = data.get('phrase')
    score = data.get('score', 0)  # This would come from speech recognition analysis
    
    # Update user progress
    if 'progress' not in session:
        session['progress'] = {}
    
    if 'pronunciation_scores' not in session['progress']:
        session['progress']['pronunciation_scores'] = {}
    
    session['progress']['pronunciation_scores'][phrase] = score
    session['progress']['total_score'] = sum(session['progress']['pronunciation_scores'].values())
    
    # Mark session as modified
    session.modified = True
    
    return jsonify({
        'success': True,
        'score': score,
        'total_score': session['progress']['total_score']
    })

@app.route('/api/complete_lesson', methods=['POST'])
def complete_lesson():
    data = request.get_json()
    lesson_id = data.get('lesson_id')
    level = data.get('level')
    
    if 'progress' not in session:
        session['progress'] = {}
    
    if 'completed_lessons' not in session['progress']:
        session['progress']['completed_lessons'] = []
    
    lesson_key = f"{level}_{lesson_id}"
    if lesson_key not in session['progress']['completed_lessons']:
        session['progress']['completed_lessons'].append(lesson_key)
    
    session.modified = True
    
    return jsonify({
        'success': True,
        'completed_lessons': len(session['progress']['completed_lessons'])
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)