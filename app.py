from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
import json

app = Flask(__name__)
app.secret_key = 'english_learning_secret_key'

# Sample data for learning activities
vocabulary_words = [
    {
        "word": "ameliorate",
        "definition": "to make or become better; improve",
        "synonyms": ["improve", "enhance", "better"],
        "example": "The new policies helped ameliorate the housing crisis."
    },
    {
        "word": "ubiquitous",
        "definition": "present, appearing, or found everywhere",
        "synonyms": ["omnipresent", "pervasive", "universal"],
        "example": "Smartphones have become ubiquitous in modern society."
    },
    {
        "word": "ephemeral",
        "definition": "lasting for a very short time",
        "synonyms": ["temporary", "fleeting", "transient"],
        "example": "The beauty of cherry blossoms is ephemeral."
    },
    {
        "word": "pragmatic",
        "definition": "dealing with things sensibly and realistically",
        "synonyms": ["practical", "realistic", "sensible"],
        "example": "She took a pragmatic approach to solving the problem."
    },
    {
        "word": "eloquent",
        "definition": "fluent or persuasive in speaking or writing",
        "synonyms": ["articulate", "fluent", "expressive"],
        "example": "The speaker gave an eloquent presentation."
    }
]

grammar_exercises = [
    {
        "question": "Choose the correct form: She ____ to the store yesterday.",
        "options": ["go", "goes", "went", "gone"],
        "correct": 2,
        "explanation": "Past tense is needed for 'yesterday'"
    },
    {
        "question": "Fill in the blank: If I ____ rich, I would travel the world.",
        "options": ["am", "was", "were", "be"],
        "correct": 2,
        "explanation": "Use 'were' in hypothetical conditional statements"
    },
    {
        "question": "Choose the correct: The book ____ on the table belongs to me.",
        "options": ["laying", "lying", "lay", "lie"],
        "correct": 1,
        "explanation": "'Lying' is the present participle of 'lie' (to be in a position)"
    },
    {
        "question": "Select the right option: Neither the teacher nor the students ____ present.",
        "options": ["was", "were", "is", "are"],
        "correct": 1,
        "explanation": "When using 'neither...nor', verb agrees with the nearest subject"
    }
]

reading_passages = [
    {
        "title": "The Benefits of Reading",
        "text": "Reading is one of the most beneficial activities for the human mind. It expands vocabulary, improves concentration, and enhances critical thinking skills. Regular reading can reduce stress levels and improve empathy by allowing readers to experience different perspectives. Studies have shown that people who read regularly have better memory retention and are less likely to develop cognitive decline as they age.",
        "questions": [
            {
                "question": "According to the passage, reading can:",
                "options": ["Only improve vocabulary", "Reduce stress and improve empathy", "Cause cognitive decline", "Decrease concentration"],
                "correct": 1
            },
            {
                "question": "What effect does reading have on memory?",
                "options": ["It has no effect", "It improves retention", "It causes memory loss", "It only affects short-term memory"],
                "correct": 1
            }
        ]
    }
]

writing_prompts = [
    "Describe a world where colors have disappeared. How do people adapt?",
    "Write about a conversation between you and your future self.",
    "Imagine you can communicate with animals for one day. What happens?",
    "Describe the perfect city from your perspective.",
    "Write about a memory that changed your perspective on life.",
    "Create a story about finding a mysterious object in your backyard.",
    "Describe what happens when time moves backwards for a day.",
    "Write about a world where music is forbidden."
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vocabulary')
def vocabulary():
    # Get a random word if not specified
    word_index = request.args.get('word', type=int)
    if word_index is None:
        word_index = random.randint(0, len(vocabulary_words) - 1)
    
    word = vocabulary_words[word_index]
    total_words = len(vocabulary_words)
    
    return render_template('vocabulary.html', word=word, word_index=word_index, total_words=total_words)

@app.route('/grammar')
def grammar():
    exercise_index = request.args.get('exercise', type=int)
    if exercise_index is None:
        exercise_index = random.randint(0, len(grammar_exercises) - 1)
    
    exercise = grammar_exercises[exercise_index]
    total_exercises = len(grammar_exercises)
    
    return render_template('grammar.html', exercise=exercise, exercise_index=exercise_index, total_exercises=total_exercises)

@app.route('/check_grammar', methods=['POST'])
def check_grammar():
    exercise_index = int(request.form['exercise_index'])
    user_answer = int(request.form['answer'])
    
    exercise = grammar_exercises[exercise_index]
    correct = user_answer == exercise['correct']
    
    return jsonify({
        'correct': correct,
        'explanation': exercise['explanation'],
        'correct_answer': exercise['options'][exercise['correct']]
    })

@app.route('/reading')
def reading():
    passage_index = request.args.get('passage', type=int)
    if passage_index is None:
        passage_index = random.randint(0, len(reading_passages) - 1)
    
    passage = reading_passages[passage_index]
    
    return render_template('reading.html', passage=passage, passage_index=passage_index)

@app.route('/check_reading', methods=['POST'])
def check_reading():
    passage_index = int(request.form['passage_index'])
    answers = request.form.getlist('answer')
    
    passage = reading_passages[passage_index]
    results = []
    
    for i, answer in enumerate(answers):
        if i < len(passage['questions']):
            correct = int(answer) == passage['questions'][i]['correct']
            results.append({
                'question': passage['questions'][i]['question'],
                'correct': correct,
                'user_answer': passage['questions'][i]['options'][int(answer)],
                'correct_answer': passage['questions'][i]['options'][passage['questions'][i]['correct']]
            })
    
    return jsonify({'results': results})

@app.route('/writing')
def writing():
    prompt = random.choice(writing_prompts)
    return render_template('writing.html', prompt=prompt)

@app.route('/new_prompt')
def new_prompt():
    prompt = random.choice(writing_prompts)
    return jsonify({'prompt': prompt})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)