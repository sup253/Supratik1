# English Speaking Practice App

A comprehensive Python application designed to help users improve their English speaking skills through interactive exercises and real-time feedback.

## Features

### 🎯 Four Main Practice Modes

1. **Pronunciation Practice**
   - Listen to common English phrases
   - Record your pronunciation and get instant feedback
   - Compare your speech with target phrases
   - Progress tracking with accuracy scores

2. **Vocabulary Practice**
   - Learn new words with definitions
   - Practice pronunciation of individual words
   - Interactive word recognition challenges
   - Expand your vocabulary systematically

3. **Conversation Practice**
   - 30-second speaking challenges on various topics
   - Real-time speech-to-text transcription
   - Practice fluency and spontaneous speaking
   - Topics include hobbies, family, travel, and more

4. **Progress Tracking**
   - View your speaking accuracy statistics
   - Track total practice sessions
   - Get helpful speaking tips and techniques
   - Monitor your improvement over time

## Installation

### Prerequisites

- Python 3.7 or higher
- Microphone access for speech recognition
- Internet connection for Google Speech Recognition API

### Setup Instructions

1. **Clone or download the application:**
   ```bash
   # If you have git installed
   git clone <repository-url>
   
   # Or download the files directly
   ```

2. **Install system dependencies (Linux/Ubuntu):**
   ```bash
   sudo apt update
   sudo apt install python3.13-venv python3-pip portaudio19-dev
   ```

3. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

5. **For other operating systems:**
   - **macOS:** `brew install portaudio` then follow steps 3-4
   - **Windows:** PyAudio should install automatically, just follow steps 3-4

## Usage

### Running the Application

**Option 1: Using the launcher (recommended):**
```bash
python run.py
```

**Option 2: Direct execution:**
```bash
source venv/bin/activate  # Activate virtual environment first
python english_speaking_app.py
```

### Using the Features

#### Pronunciation Practice
1. Click "New Phrase" to get a random phrase
2. Click "🔊 Listen" to hear the correct pronunciation
3. Click "🎤 Record & Check" to practice speaking
4. Get instant feedback on your pronunciation accuracy

#### Vocabulary Practice
1. Click "New Word" to see a vocabulary word with definition
2. Click "🔊 Pronounce" to hear the word
3. Click "🎤 Practice" to test your pronunciation
4. Receive feedback on your attempt

#### Conversation Practice
1. Click "New Topic" to get a conversation starter
2. Click "🎤 Start Speaking" to begin 30-second practice
3. Speak continuously about the topic
4. View real-time transcription of your speech

#### Progress Tracking
- View your overall accuracy score
- See total number of practice sessions
- Read helpful speaking tips and techniques

## Technical Details

### Dependencies

- **pyttsx3**: Text-to-speech conversion
- **SpeechRecognition**: Speech-to-text conversion
- **pyaudio**: Audio recording and playback
- **tkinter**: GUI framework (included with Python)

### Features Overview

- **Real-time Speech Recognition**: Uses Google's Speech Recognition API
- **Text-to-Speech**: Converts text to natural-sounding speech
- **Similarity Matching**: Compares your speech with target phrases
- **Progress Tracking**: Saves and displays your improvement statistics
- **Multi-threaded**: Prevents GUI freezing during audio operations

## Troubleshooting

### Common Issues

1. **Virtual Environment Issues:**
   - Make sure to activate the virtual environment before running
   - On Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`

2. **Microphone not working:**
   - Check if your microphone is connected and working
   - Ensure the application has microphone permissions
   - Try adjusting microphone sensitivity in system settings

3. **Speech recognition errors:**
   - Ensure you have a stable internet connection
   - Speak clearly and at a moderate pace
   - Check if background noise is interfering

4. **Installation issues:**
   - Make sure you have Python 3.7+ installed
   - Install system dependencies first (portaudio19-dev on Linux)
   - Try installing packages one by one if bulk installation fails

### Performance Tips

- Use the app in a quiet environment for best results
- Speak at a normal conversational pace
- Position your microphone at an appropriate distance
- Practice regularly for better results

## Educational Benefits

### What You'll Improve

- **Pronunciation**: Clear and accurate speech sounds
- **Fluency**: Smooth and natural speech flow
- **Vocabulary**: Expanded word knowledge and usage
- **Confidence**: Regular practice builds speaking confidence
- **Listening Skills**: Enhanced through audio feedback

### Learning Methodology

The app uses proven language learning techniques:
- **Repetition**: Practice phrases multiple times
- **Immediate Feedback**: Get instant results on pronunciation
- **Varied Practice**: Different types of speaking exercises
- **Progress Tracking**: Monitor improvement over time

## Customization

### Adding Your Own Content

You can easily customize the practice content by editing these lists in the code:

- `common_phrases`: Add your own phrases for pronunciation practice
- `vocabulary_words`: Add new words with definitions
- `conversation_starters`: Add topics for conversation practice

### Adjusting Speech Settings

Modify TTS settings in the code:
- `rate`: Speech speed (default: 150)
- `volume`: Speech volume (default: 0.9)

## Future Enhancements

Potential features for future versions:
- Offline speech recognition
- More sophisticated pronunciation analysis
- Recording playback for self-evaluation
- Difficulty levels for different skill levels
- Progress export and sharing features

## License

This application is created for educational purposes. Please ensure you comply with the terms of service for Google Speech Recognition API if using extensively.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are correctly installed
3. Verify microphone and internet connectivity
4. Make sure virtual environment is activated

---

Happy practicing! 🎉 Regular use of this app will help you improve your English speaking skills effectively.