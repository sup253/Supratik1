#!/usr/bin/env python3
"""
Simple English Speaking Practice App
A web-based application to improve English speaking skills
"""

import pyttsx3
import threading
import random
import time
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import webbrowser

class EnglishSpeakingApp:
    def __init__(self):
        # Initialize TTS engine
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)
            self.tts_available = True
        except Exception as e:
            print(f"Text-to-speech not available: {e}")
            self.tts_available = False
        
        # Initialize speech recognition (optional)
        self.speech_available = False
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.speech_available = True
        except ImportError:
            print("Speech recognition not available - audio recording disabled")
        except Exception as e:
            print(f"Speech recognition error: {e}")
        
        # Practice data
        self.common_phrases = [
            "Hello, how are you today?",
            "Nice to meet you.",
            "Could you please help me?",
            "I would like to order coffee.",
            "What time is it?",
            "Where is the nearest bank?",
            "Thank you very much.",
            "Have a great day!",
            "I'm sorry, I don't understand.",
            "Can you speak more slowly?",
            "How much does this cost?",
            "I'm learning English.",
            "What's the weather like?",
            "I need to practice my pronunciation.",
            "This is a beautiful place.",
            "Could you repeat that please?",
            "I'd like to make a reservation.",
            "What's your favorite food?",
            "The weather is nice today.",
            "I'm looking for a job."
        ]
        
        self.vocabulary_words = [
            {"word": "apple", "definition": "A red or green fruit", "example": "I eat an apple every day."},
            {"word": "beautiful", "definition": "Pleasant to look at", "example": "The sunset is beautiful."},
            {"word": "computer", "definition": "Electronic device for processing data", "example": "I use my computer for work."},
            {"word": "education", "definition": "The process of learning", "example": "Education is very important."},
            {"word": "friendship", "definition": "A close relationship between people", "example": "Their friendship lasted for years."},
            {"word": "government", "definition": "The system that rules a country", "example": "The government makes laws."},
            {"word": "happiness", "definition": "The feeling of joy", "example": "Money can't buy happiness."},
            {"word": "important", "definition": "Having great significance", "example": "This meeting is very important."},
            {"word": "journey", "definition": "A trip from one place to another", "example": "The journey took three hours."},
            {"word": "knowledge", "definition": "Information and understanding", "example": "Knowledge is power."},
            {"word": "language", "definition": "A system of communication", "example": "English is a global language."},
            {"word": "mountain", "definition": "A large natural elevation", "example": "The mountain is very high."},
            {"word": "necessary", "definition": "Required or needed", "example": "Water is necessary for life."},
            {"word": "opportunity", "definition": "A chance to do something", "example": "This is a great opportunity."},
            {"word": "peaceful", "definition": "Calm and quiet", "example": "The village is very peaceful."}
        ]
        
        self.conversation_topics = [
            "Tell me about your hobbies and interests.",
            "What did you do yesterday?",
            "Describe your favorite food and why you like it.",
            "What are your future plans and goals?",
            "Tell me about your family.",
            "What's your favorite season and why?",
            "Describe your hometown or city.",
            "What kind of music do you like?",
            "Tell me about a memorable trip or vacation.",
            "What skills would you like to learn?",
            "Describe a typical day in your life.",
            "What's your dream job?",
            "Tell me about your favorite book or movie.",
            "What makes you happy?",
            "Describe your best friend."
        ]
        
        self.current_phrase = ""
        self.current_word = {}
        self.current_topic = ""
        self.score = 0
        self.attempts = 0
        
    def speak_text(self, text):
        """Convert text to speech"""
        if self.tts_available:
            def speak():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            thread = threading.Thread(target=speak)
            thread.daemon = True
            thread.start()
            return True
        return False
    
    def get_random_phrase(self):
        """Get a random phrase for practice"""
        self.current_phrase = random.choice(self.common_phrases)
        return self.current_phrase
    
    def get_random_word(self):
        """Get a random vocabulary word"""
        self.current_word = random.choice(self.vocabulary_words)
        return self.current_word
    
    def get_random_topic(self):
        """Get a random conversation topic"""
        self.current_topic = random.choice(self.conversation_topics)
        return self.current_topic
    
    def mark_practice_complete(self):
        """Mark a practice session as complete"""
        self.attempts += 1
        self.score += 1
        return {
            "score": self.score,
            "attempts": self.attempts,
            "accuracy": round((self.score / self.attempts) * 100, 1) if self.attempts > 0 else 0
        }

# Global app instance
app = EnglishSpeakingApp()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_html_page().encode())
        elif self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_api_request(self):
        try:
            if self.path == '/api/speak':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '')
                
                success = app.speak_text(text)
                self.send_json_response({'success': success})
                
            elif self.path == '/api/phrase':
                phrase = app.get_random_phrase()
                self.send_json_response({'phrase': phrase})
                
            elif self.path == '/api/word':
                word = app.get_random_word()
                self.send_json_response({'word': word})
                
            elif self.path == '/api/topic':
                topic = app.get_random_topic()
                self.send_json_response({'topic': topic})
                
            elif self.path == '/api/complete':
                progress = app.mark_practice_complete()
                self.send_json_response({'progress': progress})
                
            elif self.path == '/api/status':
                status = {
                    'tts_available': app.tts_available,
                    'speech_available': app.speech_available,
                    'score': app.score,
                    'attempts': app.attempts,
                    'accuracy': round((app.score / app.attempts) * 100, 1) if app.attempts > 0 else 0
                }
                self.send_json_response(status)
                
            else:
                self.send_response(404)
                self.end_headers()
                
        except Exception as e:
            self.send_json_response({'error': str(e)}, status=500)
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def get_html_page(self):
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>English Speaking Practice App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .tabs {
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #dee2e6;
        }
        
        .tab {
            flex: 1;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
            font-size: 1.1em;
        }
        
        .tab:hover {
            background: #e9ecef;
        }
        
        .tab.active {
            background: #3498db;
            color: white;
        }
        
        .content {
            padding: 40px;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .practice-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            border: 2px solid #dee2e6;
            transition: all 0.3s ease;
        }
        
        .practice-card:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        
        .practice-text {
            font-size: 1.4em;
            text-align: center;
            margin: 20px 0;
            padding: 20px;
            background: white;
            border-radius: 10px;
            border: 2px solid #e9ecef;
            min-height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #2c3e50;
        }
        
        .buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 20px 0;
        }
        
        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .btn-primary {
            background: #3498db;
            color: white;
        }
        
        .btn-success {
            background: #27ae60;
            color: white;
        }
        
        .btn-warning {
            background: #f39c12;
            color: white;
        }
        
        .btn-danger {
            background: #e74c3c;
            color: white;
        }
        
        .btn-info {
            background: #17a2b8;
            color: white;
        }
        
        .feedback {
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            border-radius: 10px;
            font-size: 1.1em;
            font-weight: bold;
            min-height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .feedback.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .feedback.info {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        .word-details {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #3498db;
        }
        
        .word-definition {
            font-size: 1.1em;
            color: #666;
            margin: 10px 0;
        }
        
        .word-example {
            font-style: italic;
            color: #888;
            margin: 10px 0;
        }
        
        .progress-stats {
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
        }
        
        .stat-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            border: 2px solid #dee2e6;
            min-width: 200px;
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
        }
        
        .stat-label {
            font-size: 1.1em;
            color: #666;
            margin-top: 10px;
        }
        
        .tips-section {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
        }
        
        .tips-section h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .tips-section ul {
            padding-left: 20px;
        }
        
        .tips-section li {
            margin: 10px 0;
            font-size: 1.1em;
            line-height: 1.5;
        }
        
        .status-indicator {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            text-align: center;
            font-weight: bold;
        }
        
        .status-success {
            background: #d4edda;
            color: #155724;
        }
        
        .status-warning {
            background: #fff3cd;
            color: #856404;
        }
        
        .timer {
            font-size: 1.5em;
            font-weight: bold;
            color: #e74c3c;
            text-align: center;
            margin: 20px 0;
        }
        
        @media (max-width: 768px) {
            .tabs {
                flex-direction: column;
            }
            
            .buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .btn {
                width: 100%;
                max-width: 300px;
            }
            
            .progress-stats {
                flex-direction: column;
                gap: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 English Speaking Practice</h1>
            <p>Improve your English speaking skills with interactive exercises</p>
        </div>
        
        <div class="tabs">
            <div class="tab active" onclick="showTab('pronunciation')">Pronunciation</div>
            <div class="tab" onclick="showTab('vocabulary')">Vocabulary</div>
            <div class="tab" onclick="showTab('conversation')">Conversation</div>
            <div class="tab" onclick="showTab('progress')">Progress</div>
        </div>
        
        <div class="content">
            <!-- Pronunciation Tab -->
            <div id="pronunciation" class="tab-content active">
                <div class="practice-card">
                    <h2>Pronunciation Practice</h2>
                    <p>Practice pronunciation with common phrases. Click "Listen" to hear the phrase, then practice speaking it aloud.</p>
                    <div class="practice-text" id="phrase-text">Click "New Phrase" to start!</div>
                    <div class="buttons">
                        <button class="btn btn-primary" onclick="newPhrase()">New Phrase</button>
                        <button class="btn btn-success" onclick="speakPhrase()">🔊 Listen</button>
                        <button class="btn btn-warning" onclick="markPracticed('pronunciation')">✓ Mark as Practiced</button>
                    </div>
                    <div class="feedback" id="pronunciation-feedback"></div>
                </div>
            </div>
            
            <!-- Vocabulary Tab -->
            <div id="vocabulary" class="tab-content">
                <div class="practice-card">
                    <h2>Vocabulary Practice</h2>
                    <p>Learn new vocabulary words with definitions and examples. Practice pronunciation and usage.</p>
                    <div class="practice-text" id="word-text">Click "New Word" to start!</div>
                    <div class="word-details" id="word-details" style="display: none;">
                        <div class="word-definition" id="word-definition"></div>
                        <div class="word-example" id="word-example"></div>
                    </div>
                    <div class="buttons">
                        <button class="btn btn-primary" onclick="newWord()">New Word</button>
                        <button class="btn btn-success" onclick="speakWord()">🔊 Pronounce</button>
                        <button class="btn btn-warning" onclick="markPracticed('vocabulary')">✓ Mark as Practiced</button>
                    </div>
                    <div class="feedback" id="vocabulary-feedback"></div>
                </div>
            </div>
            
            <!-- Conversation Tab -->
            <div id="conversation" class="tab-content">
                <div class="practice-card">
                    <h2>Conversation Practice</h2>
                    <p>Practice speaking about different topics. You have 60 seconds to speak about each topic.</p>
                    <div class="practice-text" id="topic-text">Click "New Topic" to start!</div>
                    <div class="timer" id="timer"></div>
                    <div class="buttons">
                        <button class="btn btn-primary" onclick="newTopic()">New Topic</button>
                        <button class="btn btn-danger" onclick="startConversation()">⏱️ Start 60s Practice</button>
                    </div>
                    <div class="feedback" id="conversation-feedback"></div>
                </div>
            </div>
            
            <!-- Progress Tab -->
            <div id="progress" class="tab-content">
                <div class="practice-card">
                    <h2>Your Progress</h2>
                    <div class="progress-stats">
                        <div class="stat-card">
                            <div class="stat-number" id="score">0</div>
                            <div class="stat-label">Score</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="attempts">0</div>
                            <div class="stat-label">Attempts</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number" id="accuracy">0%</div>
                            <div class="stat-label">Accuracy</div>
                        </div>
                    </div>
                    
                    <div class="tips-section">
                        <h3>💡 Speaking Tips</h3>
                        <ul>
                            <li>Practice speaking slowly and clearly</li>
                            <li>Listen to native speakers and try to imitate their pronunciation</li>
                            <li>Don't be afraid to make mistakes - they're part of learning!</li>
                            <li>Practice regularly, even if just for a few minutes each day</li>
                            <li>Focus on common words and phrases first</li>
                            <li>Use gestures and facial expressions to help convey meaning</li>
                            <li>Record yourself speaking and listen back to identify improvements</li>
                            <li>Join conversation groups or find speaking partners</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Global variables
        let currentPhrase = '';
        let currentWord = {};
        let currentTopic = '';
        let timer = null;
        
        // Initialize the app
        window.onload = function() {
            checkStatus();
            newPhrase();
            newWord();
            newTopic();
        };
        
        // Tab switching
        function showTab(tabName) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            // Remove active class from all tabs
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab content
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
            
            // Update progress when switching to progress tab
            if (tabName === 'progress') {
                updateProgress();
            }
        }
        
        // API functions
        async function apiCall(endpoint, data = null) {
            const options = {
                method: data ? 'POST' : 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            };
            
            if (data) {
                options.body = JSON.stringify(data);
            }
            
            const response = await fetch(endpoint, options);
            return await response.json();
        }
        
        // Check app status
        async function checkStatus() {
            try {
                const status = await apiCall('/api/status');
                if (!status.tts_available) {
                    document.querySelectorAll('.btn-success').forEach(btn => {
                        btn.disabled = true;
                        btn.style.opacity = '0.5';
                    });
                }
            } catch (error) {
                console.error('Status check failed:', error);
            }
        }
        
        // Pronunciation practice
        async function newPhrase() {
            try {
                const response = await apiCall('/api/phrase');
                currentPhrase = response.phrase;
                document.getElementById('phrase-text').textContent = currentPhrase;
                showFeedback('pronunciation', 'Click "Listen" to hear the pronunciation, then practice speaking aloud!', 'info');
            } catch (error) {
                console.error('Failed to get new phrase:', error);
            }
        }
        
        async function speakPhrase() {
            try {
                await apiCall('/api/speak', { text: currentPhrase });
                showFeedback('pronunciation', 'Now practice saying: "' + currentPhrase + '"', 'info');
            } catch (error) {
                console.error('Failed to speak phrase:', error);
                showFeedback('pronunciation', 'Text-to-speech not available', 'info');
            }
        }
        
        // Vocabulary practice
        async function newWord() {
            try {
                const response = await apiCall('/api/word');
                currentWord = response.word;
                document.getElementById('word-text').textContent = currentWord.word.toUpperCase();
                document.getElementById('word-definition').textContent = currentWord.definition;
                document.getElementById('word-example').textContent = 'Example: ' + currentWord.example;
                document.getElementById('word-details').style.display = 'block';
                showFeedback('vocabulary', 'Click "Pronounce" to hear the word, then practice speaking it!', 'info');
            } catch (error) {
                console.error('Failed to get new word:', error);
            }
        }
        
        async function speakWord() {
            try {
                await apiCall('/api/speak', { text: currentWord.word });
                showFeedback('vocabulary', 'Now practice saying: "' + currentWord.word + '"', 'info');
            } catch (error) {
                console.error('Failed to speak word:', error);
                showFeedback('vocabulary', 'Text-to-speech not available', 'info');
            }
        }
        
        // Conversation practice
        async function newTopic() {
            try {
                const response = await apiCall('/api/topic');
                currentTopic = response.topic;
                document.getElementById('topic-text').textContent = currentTopic;
                document.getElementById('timer').textContent = 'Press "Start 60s Practice" to begin!';
                showFeedback('conversation', 'New topic ready! Click start when you\'re ready to practice.', 'info');
            } catch (error) {
                console.error('Failed to get new topic:', error);
            }
        }
        
        function startConversation() {
            let timeLeft = 60;
            document.getElementById('timer').textContent = `Time remaining: ${timeLeft} seconds`;
            showFeedback('conversation', 'Timer started! Speak about the topic for 60 seconds.', 'info');
            
            timer = setInterval(() => {
                timeLeft--;
                document.getElementById('timer').textContent = `Time remaining: ${timeLeft} seconds`;
                
                if (timeLeft <= 0) {
                    clearInterval(timer);
                    document.getElementById('timer').textContent = "Time's up! Great job practicing!";
                    showFeedback('conversation', 'Excellent! You practiced for 60 seconds. Keep up the good work!', 'success');
                    markPracticed('conversation');
                }
            }, 1000);
        }
        
        // Mark practice as complete
        async function markPracticed(type) {
            try {
                const response = await apiCall('/api/complete');
                const progress = response.progress;
                
                let message = '';
                switch (type) {
                    case 'pronunciation':
                        message = 'Great job practicing pronunciation! ✅';
                        break;
                    case 'vocabulary':
                        message = `Great job learning "${currentWord.word}"! ✅`;
                        break;
                    case 'conversation':
                        message = 'Excellent conversation practice! ✅';
                        break;
                }
                
                showFeedback(type, message, 'success');
                updateProgress();
            } catch (error) {
                console.error('Failed to mark practice complete:', error);
            }
        }
        
        // Update progress display
        async function updateProgress() {
            try {
                const status = await apiCall('/api/status');
                document.getElementById('score').textContent = status.score;
                document.getElementById('attempts').textContent = status.attempts;
                document.getElementById('accuracy').textContent = status.accuracy + '%';
            } catch (error) {
                console.error('Failed to update progress:', error);
            }
        }
        
        // Show feedback messages
        function showFeedback(type, message, kind = 'info') {
            const feedbackElement = document.getElementById(type + '-feedback');
            feedbackElement.textContent = message;
            feedbackElement.className = 'feedback ' + kind;
        }
    </script>
</body>
</html>
        """

def main():
    PORT = 8000
    
    print("🎯 English Speaking Practice App")
    print("=" * 50)
    print(f"Starting web server on port {PORT}...")
    print(f"Open your browser and go to: http://localhost:{PORT}")
    print()
    print("Features:")
    print("• Pronunciation practice with common phrases")
    print("• Vocabulary learning with definitions and examples")
    print("• Conversation practice with timed exercises")
    print("• Progress tracking and speaking tips")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    server = HTTPServer(('localhost', PORT), RequestHandler)
    
    try:
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            pass
        
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()

if __name__ == "__main__":
    main()