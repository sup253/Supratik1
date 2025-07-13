#!/usr/bin/env python3
"""
English Speaking Practice App - Command Line Interface
A simple CLI version for practicing English speaking skills
"""

import pyttsx3
import threading
import random
import time
import sys

class EnglishSpeakingCLI:
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
        
        self.score = 0
        self.attempts = 0
        
    def speak_text(self, text):
        """Speak the given text using TTS"""
        if self.tts_available:
            def speak():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            thread = threading.Thread(target=speak)
            thread.daemon = True
            thread.start()
            thread.join()  # Wait for speech to complete
        else:
            print(f"[TTS would say: {text}]")
    
    def pronunciation_practice(self):
        """Practice pronunciation with phrases"""
        print("\n🎯 PRONUNCIATION PRACTICE")
        print("=" * 50)
        
        phrase = random.choice(self.common_phrases)
        print(f"\nPhrase: {phrase}")
        
        while True:
            print("\nOptions:")
            print("1. Listen to pronunciation")
            print("2. Mark as practiced")
            print("3. Get new phrase")
            print("4. Back to main menu")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                print("🔊 Playing pronunciation...")
                self.speak_text(phrase)
                
            elif choice == '2':
                self.attempts += 1
                self.score += 1
                print("✅ Great job practicing! Keep up the good work!")
                break
                
            elif choice == '3':
                phrase = random.choice(self.common_phrases)
                print(f"\nNew phrase: {phrase}")
                
            elif choice == '4':
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
    
    def vocabulary_practice(self):
        """Practice vocabulary words"""
        print("\n📚 VOCABULARY PRACTICE")
        print("=" * 50)
        
        word, definition = random.choice(self.vocabulary_words)
        print(f"\nWord: {word.upper()}")
        print(f"Definition: {definition}")
        
        while True:
            print("\nOptions:")
            print("1. Listen to pronunciation")
            print("2. Mark as practiced")
            print("3. Get new word")
            print("4. Back to main menu")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                print("🔊 Playing pronunciation...")
                self.speak_text(word)
                
            elif choice == '2':
                self.attempts += 1
                self.score += 1
                print(f"✅ Great job practicing '{word}'!")
                break
                
            elif choice == '3':
                word, definition = random.choice(self.vocabulary_words)
                print(f"\nNew word: {word.upper()}")
                print(f"Definition: {definition}")
                
            elif choice == '4':
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
    
    def conversation_practice(self):
        """Practice conversation topics"""
        print("\n💬 CONVERSATION PRACTICE")
        print("=" * 50)
        
        topic = random.choice(self.conversation_starters)
        print(f"\nTopic: {topic}")
        
        while True:
            print("\nOptions:")
            print("1. Start 30-second practice")
            print("2. Get new topic")
            print("3. Back to main menu")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                print(f"\n⏱️ Starting 30-second practice on: {topic}")
                print("Speak aloud about this topic now!")
                
                # 30-second countdown
                for i in range(30, 0, -1):
                    print(f"\rTime remaining: {i:2d} seconds", end="", flush=True)
                    time.sleep(1)
                
                print("\n\n✅ Time's up! Great job practicing!")
                self.attempts += 1
                self.score += 1
                break
                
            elif choice == '2':
                topic = random.choice(self.conversation_starters)
                print(f"\nNew topic: {topic}")
                
            elif choice == '3':
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
    
    def show_progress(self):
        """Show practice progress"""
        print("\n📊 YOUR PROGRESS")
        print("=" * 50)
        
        accuracy = (self.score / self.attempts * 100) if self.attempts > 0 else 0
        print(f"Score: {self.score} / {self.attempts} (Accuracy: {accuracy:.1f}%)")
        print(f"Total Practice Sessions: {self.attempts}")
        
        print("\n💡 SPEAKING TIPS:")
        print("• Practice speaking slowly and clearly")
        print("• Listen to native speakers and imitate their pronunciation")
        print("• Don't be afraid to make mistakes - they're part of learning!")
        print("• Practice regularly, even if just for a few minutes each day")
        print("• Focus on common words and phrases first")
        print("• Use gestures and facial expressions to help convey meaning")
        print("• Join conversation groups or find speaking partners")
        print("• Watch movies and TV shows in English with subtitles")
        print("• Read aloud to practice pronunciation and fluency")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        print("🎯 ENGLISH SPEAKING PRACTICE APP")
        print("=" * 50)
        print("Welcome to your English speaking practice session!")
        
        if not self.tts_available:
            print("⚠️ Text-to-speech is not available - you'll see text instead of hearing audio.")
        
        while True:
            print("\n📋 MAIN MENU")
            print("1. Pronunciation Practice")
            print("2. Vocabulary Practice")
            print("3. Conversation Practice")
            print("4. View Progress")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                self.pronunciation_practice()
                
            elif choice == '2':
                self.vocabulary_practice()
                
            elif choice == '3':
                self.conversation_practice()
                
            elif choice == '4':
                self.show_progress()
                
            elif choice == '5':
                print("\n🎉 Thank you for practicing! Keep up the great work!")
                break
                
            else:
                print("❌ Invalid choice. Please try again.")

def main():
    app = EnglishSpeakingCLI()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Keep practicing your English!")
        sys.exit(0)

if __name__ == "__main__":
    main()