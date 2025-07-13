import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyttsx3
import threading
import random
import time

# Try to import speech recognition, but handle gracefully if it fails
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("Speech recognition not available. Audio recording features will be disabled.")

class EnglishSpeakingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("English Speaking Practice App")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
        # Initialize speech recognizer only if available
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                self.speech_features_enabled = True
            except Exception as e:
                print(f"Speech recognition initialization failed: {e}")
                self.speech_features_enabled = False
        else:
            self.speech_features_enabled = False
        
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
            "This is a beautiful place."
        ]
        
        self.vocabulary_words = [
            ("apple", "A red or green fruit"),
            ("beautiful", "Pleasant to look at"),
            ("computer", "Electronic device for processing data"),
            ("education", "The process of learning"),
            ("friendship", "A close relationship between people"),
            ("government", "The system that rules a country"),
            ("happiness", "The feeling of joy"),
            ("important", "Having great significance"),
            ("journey", "A trip from one place to another"),
            ("knowledge", "Information and understanding"),
            ("language", "A system of communication"),
            ("mountain", "A large natural elevation"),
            ("necessary", "Required or needed"),
            ("opportunity", "A chance to do something"),
            ("peaceful", "Calm and quiet")
        ]
        
        self.conversation_starters = [
            "Tell me about your hobbies.",
            "What did you do yesterday?",
            "Describe your favorite food.",
            "What are your future plans?",
            "Tell me about your family.",
            "What's your favorite season and why?",
            "Describe your hometown.",
            "What kind of music do you like?",
            "Tell me about a memorable trip.",
            "What skills would you like to learn?"
        ]
        
        self.current_exercise = ""
        self.score = 0
        self.attempts = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="English Speaking Practice App", 
                              font=("Arial", 20, "bold"), bg='#f0f0f0', fg='#2c3e50')
        title_label.pack(pady=10)
        
        # Show speech recognition status
        if not self.speech_features_enabled:
            status_label = tk.Label(self.root, text="⚠️ Speech recognition disabled - Audio features not available", 
                                  font=("Arial", 10), bg='#f0f0f0', fg='#e74c3c')
            status_label.pack(pady=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Pronunciation Practice Tab
        self.pronunciation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pronunciation_frame, text="Pronunciation Practice")
        self.setup_pronunciation_tab()
        
        # Vocabulary Tab
        self.vocabulary_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.vocabulary_frame, text="Vocabulary Practice")
        self.setup_vocabulary_tab()
        
        # Conversation Tab
        self.conversation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.conversation_frame, text="Conversation Practice")
        self.setup_conversation_tab()
        
        # Progress Tab
        self.progress_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.progress_frame, text="Progress")
        self.setup_progress_tab()
        
    def setup_pronunciation_tab(self):
        # Instructions
        instructions_text = "Practice pronunciation with common phrases. Click 'Listen' to hear the phrase"
        if self.speech_features_enabled:
            instructions_text += ", then 'Record' to practice and get feedback."
        else:
            instructions_text += ". Audio recording is disabled - practice by repeating aloud."
        
        instructions = tk.Label(self.pronunciation_frame, text=instructions_text,
                               font=("Arial", 11), wraplength=700, justify='left')
        instructions.pack(pady=10, padx=20)
        
        # Current phrase display
        self.phrase_var = tk.StringVar()
        phrase_label = tk.Label(self.pronunciation_frame, textvariable=self.phrase_var,
                               font=("Arial", 14, "bold"), wraplength=600, justify='center',
                               bg='white', relief='raised', bd=2)
        phrase_label.pack(pady=20, padx=20, fill='x')
        
        # Buttons frame
        button_frame = tk.Frame(self.pronunciation_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        # Control buttons
        self.new_phrase_btn = tk.Button(button_frame, text="New Phrase", command=self.new_phrase,
                                       bg='#3498db', fg='white', font=("Arial", 12, "bold"),
                                       padx=20, pady=10)
        self.new_phrase_btn.pack(side='left', padx=10)
        
        self.listen_btn = tk.Button(button_frame, text="🔊 Listen", command=self.speak_phrase,
                                   bg='#2ecc71', fg='white', font=("Arial", 12, "bold"),
                                   padx=20, pady=10)
        self.listen_btn.pack(side='left', padx=10)
        
        if self.speech_features_enabled:
            self.record_btn = tk.Button(button_frame, text="🎤 Record & Check", command=self.record_and_check,
                                       bg='#e74c3c', fg='white', font=("Arial", 12, "bold"),
                                       padx=20, pady=10)
            self.record_btn.pack(side='left', padx=10)
        else:
            self.manual_btn = tk.Button(button_frame, text="✓ Mark as Practiced", command=self.mark_practiced,
                                       bg='#f39c12', fg='white', font=("Arial", 12, "bold"),
                                       padx=20, pady=10)
            self.manual_btn.pack(side='left', padx=10)
        
        # Feedback area
        self.feedback_var = tk.StringVar()
        feedback_label = tk.Label(self.pronunciation_frame, textvariable=self.feedback_var,
                                 font=("Arial", 12), wraplength=600, justify='center')
        feedback_label.pack(pady=20)
        
        # Initialize with first phrase
        self.new_phrase()
        
    def setup_vocabulary_tab(self):
        # Instructions
        instructions_text = "Learn new vocabulary words. Listen to pronunciation"
        if self.speech_features_enabled:
            instructions_text += " and practice saying them."
        else:
            instructions_text += ". Practice by repeating aloud."
        
        instructions = tk.Label(self.vocabulary_frame, text=instructions_text,
                               font=("Arial", 11), wraplength=700, justify='left')
        instructions.pack(pady=10, padx=20)
        
        # Word display
        self.word_var = tk.StringVar()
        word_label = tk.Label(self.vocabulary_frame, textvariable=self.word_var,
                             font=("Arial", 18, "bold"), fg='#2c3e50')
        word_label.pack(pady=10)
        
        # Definition display
        self.definition_var = tk.StringVar()
        definition_label = tk.Label(self.vocabulary_frame, textvariable=self.definition_var,
                                   font=("Arial", 12), wraplength=600, justify='center',
                                   bg='white', relief='raised', bd=2)
        definition_label.pack(pady=10, padx=20, fill='x')
        
        # Vocabulary buttons
        vocab_button_frame = tk.Frame(self.vocabulary_frame, bg='#f0f0f0')
        vocab_button_frame.pack(pady=20)
        
        self.new_word_btn = tk.Button(vocab_button_frame, text="New Word", command=self.new_vocabulary_word,
                                     bg='#9b59b6', fg='white', font=("Arial", 12, "bold"),
                                     padx=20, pady=10)
        self.new_word_btn.pack(side='left', padx=10)
        
        self.speak_word_btn = tk.Button(vocab_button_frame, text="🔊 Pronounce", command=self.speak_word,
                                       bg='#f39c12', fg='white', font=("Arial", 12, "bold"),
                                       padx=20, pady=10)
        self.speak_word_btn.pack(side='left', padx=10)
        
        if self.speech_features_enabled:
            self.practice_word_btn = tk.Button(vocab_button_frame, text="🎤 Practice", command=self.practice_word,
                                              bg='#e67e22', fg='white', font=("Arial", 12, "bold"),
                                              padx=20, pady=10)
            self.practice_word_btn.pack(side='left', padx=10)
        else:
            self.manual_word_btn = tk.Button(vocab_button_frame, text="✓ Mark as Practiced", command=self.mark_word_practiced,
                                            bg='#e67e22', fg='white', font=("Arial", 12, "bold"),
                                            padx=20, pady=10)
            self.manual_word_btn.pack(side='left', padx=10)
        
        # Vocabulary feedback
        self.vocab_feedback_var = tk.StringVar()
        vocab_feedback_label = tk.Label(self.vocabulary_frame, textvariable=self.vocab_feedback_var,
                                       font=("Arial", 12), wraplength=600, justify='center')
        vocab_feedback_label.pack(pady=10)
        
        # Initialize with first word
        self.new_vocabulary_word()
        
    def setup_conversation_tab(self):
        # Instructions
        instructions_text = "Practice having conversations. You'll be given topics to talk about."
        if not self.speech_features_enabled:
            instructions_text += " Speak aloud and practice for 30 seconds."
        else:
            instructions_text += " Speak for 30 seconds and get transcription."
        
        instructions = tk.Label(self.conversation_frame, text=instructions_text,
                               font=("Arial", 11), wraplength=700, justify='left')
        instructions.pack(pady=10, padx=20)
        
        # Topic display
        self.topic_var = tk.StringVar()
        topic_label = tk.Label(self.conversation_frame, textvariable=self.topic_var,
                              font=("Arial", 14, "bold"), wraplength=600, justify='center',
                              bg='white', relief='raised', bd=2)
        topic_label.pack(pady=20, padx=20, fill='x')
        
        # Timer display
        self.timer_var = tk.StringVar()
        timer_label = tk.Label(self.conversation_frame, textvariable=self.timer_var,
                              font=("Arial", 16, "bold"), fg='#e74c3c')
        timer_label.pack(pady=10)
        
        # Conversation buttons
        conv_button_frame = tk.Frame(self.conversation_frame, bg='#f0f0f0')
        conv_button_frame.pack(pady=20)
        
        self.new_topic_btn = tk.Button(conv_button_frame, text="New Topic", command=self.new_conversation_topic,
                                      bg='#1abc9c', fg='white', font=("Arial", 12, "bold"),
                                      padx=20, pady=10)
        self.new_topic_btn.pack(side='left', padx=10)
        
        start_text = "🎤 Start Speaking" if self.speech_features_enabled else "⏱️ Start Timer"
        self.start_conv_btn = tk.Button(conv_button_frame, text=start_text, command=self.start_conversation,
                                       bg='#34495e', fg='white', font=("Arial", 12, "bold"),
                                       padx=20, pady=10)
        self.start_conv_btn.pack(side='left', padx=10)
        
        # Response area
        self.response_text = scrolledtext.ScrolledText(self.conversation_frame, height=8, width=80,
                                                      font=("Arial", 10))
        self.response_text.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Initialize with first topic
        self.new_conversation_topic()
        
    def setup_progress_tab(self):
        # Progress statistics
        stats_frame = tk.LabelFrame(self.progress_frame, text="Your Progress", font=("Arial", 12, "bold"))
        stats_frame.pack(pady=20, padx=20, fill='x')
        
        self.score_var = tk.StringVar()
        score_label = tk.Label(stats_frame, textvariable=self.score_var, font=("Arial", 14))
        score_label.pack(pady=10)
        
        self.attempts_var = tk.StringVar()
        attempts_label = tk.Label(stats_frame, textvariable=self.attempts_var, font=("Arial", 14))
        attempts_label.pack(pady=5)
        
        # Tips section
        tips_frame = tk.LabelFrame(self.progress_frame, text="Speaking Tips", font=("Arial", 12, "bold"))
        tips_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        tips_text = """
• Practice speaking slowly and clearly
• Listen to native speakers and try to imitate their pronunciation
• Record yourself speaking and listen back to identify areas for improvement
• Don't be afraid to make mistakes - they're part of learning!
• Practice regularly, even if just for a few minutes each day
• Focus on common words and phrases first
• Use gestures and facial expressions to help convey meaning
• Join conversation groups or find speaking partners
• Watch movies and TV shows in English with subtitles
• Read aloud to practice pronunciation and fluency
        """
        
        tips_label = tk.Label(tips_frame, text=tips_text, font=("Arial", 10),
                             justify='left', wraplength=700)
        tips_label.pack(pady=10, padx=10)
        
        self.update_progress()
        
    def new_phrase(self):
        self.current_exercise = random.choice(self.common_phrases)
        self.phrase_var.set(self.current_exercise)
        if self.speech_features_enabled:
            self.feedback_var.set("Click 'Listen' to hear the pronunciation, then 'Record & Check' to practice!")
        else:
            self.feedback_var.set("Click 'Listen' to hear the pronunciation, then practice speaking aloud!")
        
    def speak_phrase(self):
        def speak():
            self.tts_engine.say(self.current_exercise)
            self.tts_engine.runAndWait()
        
        thread = threading.Thread(target=speak)
        thread.daemon = True
        thread.start()
        
    def mark_practiced(self):
        self.attempts += 1
        self.score += 1
        self.feedback_var.set(f"Great job practicing! Keep up the good work! ✅")
        self.update_progress()
        
    def record_and_check(self):
        def record():
            try:
                self.feedback_var.set("🎤 Listening... Speak now!")
                self.root.update()
                
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                self.feedback_var.set("Processing your speech...")
                self.root.update()
                
                try:
                    recognized_text = self.recognizer.recognize_google(audio)
                    self.attempts += 1
                    
                    # Simple comparison (you could implement more sophisticated comparison)
                    similarity = self.calculate_similarity(self.current_exercise.lower(), recognized_text.lower())
                    
                    if similarity > 0.7:
                        self.score += 1
                        self.feedback_var.set(f"Great job! You said: '{recognized_text}' ✅")
                    elif similarity > 0.4:
                        self.feedback_var.set(f"Good attempt! You said: '{recognized_text}' - Try again for better pronunciation.")
                    else:
                        self.feedback_var.set(f"You said: '{recognized_text}' - Keep practicing! The target was: '{self.current_exercise}'")
                    
                    self.update_progress()
                    
                except sr.UnknownValueError:
                    self.feedback_var.set("Sorry, I couldn't understand what you said. Please try again.")
                except sr.RequestError:
                    self.feedback_var.set("Sorry, there was an error with the speech recognition service.")
                    
            except Exception as e:
                self.feedback_var.set("Error recording audio. Please try again.")
        
        thread = threading.Thread(target=record)
        thread.daemon = True
        thread.start()
        
    def calculate_similarity(self, text1, text2):
        # Simple word-based similarity calculation
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if len(words1) == 0 and len(words2) == 0:
            return 1.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0
        
    def new_vocabulary_word(self):
        self.current_word, self.current_definition = random.choice(self.vocabulary_words)
        self.word_var.set(self.current_word.upper())
        self.definition_var.set(self.current_definition)
        if self.speech_features_enabled:
            self.vocab_feedback_var.set("Click 'Pronounce' to hear the word, then 'Practice' to try saying it!")
        else:
            self.vocab_feedback_var.set("Click 'Pronounce' to hear the word, then practice speaking it aloud!")
        
    def speak_word(self):
        def speak():
            self.tts_engine.say(self.current_word)
            self.tts_engine.runAndWait()
        
        thread = threading.Thread(target=speak)
        thread.daemon = True
        thread.start()
        
    def mark_word_practiced(self):
        self.attempts += 1
        self.score += 1
        self.vocab_feedback_var.set(f"Great job practicing '{self.current_word}'! ✅")
        self.update_progress()
        
    def practice_word(self):
        def record():
            try:
                self.vocab_feedback_var.set("🎤 Listening... Say the word!")
                self.root.update()
                
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                self.vocab_feedback_var.set("Processing...")
                self.root.update()
                
                try:
                    recognized_text = self.recognizer.recognize_google(audio)
                    self.attempts += 1
                    
                    if self.current_word.lower() in recognized_text.lower():
                        self.score += 1
                        self.vocab_feedback_var.set(f"Excellent! You said: '{recognized_text}' ✅")
                    else:
                        self.vocab_feedback_var.set(f"You said: '{recognized_text}' - The target word was: '{self.current_word}'. Try again!")
                    
                    self.update_progress()
                    
                except sr.UnknownValueError:
                    self.vocab_feedback_var.set("Sorry, I couldn't understand. Please try again.")
                except sr.RequestError:
                    self.vocab_feedback_var.set("Speech recognition service error. Please try again.")
                    
            except Exception as e:
                self.vocab_feedback_var.set("Error recording audio. Please try again.")
        
        thread = threading.Thread(target=record)
        thread.daemon = True
        thread.start()
        
    def new_conversation_topic(self):
        self.current_topic = random.choice(self.conversation_starters)
        self.topic_var.set(self.current_topic)
        if self.speech_features_enabled:
            self.timer_var.set("Press 'Start Speaking' to begin!")
        else:
            self.timer_var.set("Press 'Start Timer' to begin!")
        self.response_text.delete(1.0, tk.END)
        
    def start_conversation(self):
        def conversation_timer():
            for i in range(30, 0, -1):
                self.timer_var.set(f"Time remaining: {i} seconds")
                self.root.update()
                time.sleep(1)
            
            self.timer_var.set("Time's up! Great job practicing!")
            
        if self.speech_features_enabled:
            def record_conversation():
                try:
                    self.response_text.delete(1.0, tk.END)
                    self.response_text.insert(tk.END, "🎤 Recording started... Speak about the topic!\n\n")
                    
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        
                    # Record for 30 seconds
                    start_time = time.time()
                    full_text = ""
                    
                    while time.time() - start_time < 30:
                        try:
                            audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                            text = self.recognizer.recognize_google(audio)
                            full_text += text + " "
                            self.response_text.insert(tk.END, text + " ")
                            self.response_text.see(tk.END)
                            self.root.update()
                        except:
                            continue
                    
                    if full_text.strip():
                        self.attempts += 1
                        self.score += 1  # Award points for completing conversation practice
                        self.response_text.insert(tk.END, f"\n\n✅ Great job! You spoke for 30 seconds about: {self.current_topic}")
                    else:
                        self.response_text.insert(tk.END, "\n\nTry speaking more clearly next time!")
                    
                    self.update_progress()
                        
                except Exception as e:
                    self.response_text.insert(tk.END, f"\nError during recording: {str(e)}")
            
            # Start both timer and recording
            timer_thread = threading.Thread(target=conversation_timer)
            record_thread = threading.Thread(target=record_conversation)
            
            timer_thread.daemon = True
            record_thread.daemon = True
            
            timer_thread.start()
            record_thread.start()
        else:
            # Just start timer, no recording
            def manual_conversation():
                self.response_text.delete(1.0, tk.END)
                self.response_text.insert(tk.END, "⏱️ Timer started! Speak about the topic for 30 seconds.\n\n")
                self.response_text.insert(tk.END, f"Topic: {self.current_topic}\n\n")
                self.response_text.insert(tk.END, "Practice speaking aloud about this topic. This helps build fluency and confidence!")
                
                self.attempts += 1
                self.score += 1
                self.update_progress()
            
            timer_thread = threading.Thread(target=conversation_timer)
            manual_thread = threading.Thread(target=manual_conversation)
            
            timer_thread.daemon = True
            manual_thread.daemon = True
            
            timer_thread.start()
            manual_thread.start()
        
    def update_progress(self):
        accuracy = (self.score / self.attempts * 100) if self.attempts > 0 else 0
        self.score_var.set(f"Score: {self.score} / {self.attempts} (Accuracy: {accuracy:.1f}%)")
        self.attempts_var.set(f"Total Practice Sessions: {self.attempts}")

def main():
    root = tk.Tk()
    app = EnglishSpeakingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()