# SpeakEasy - Spoken English Learning Website

SpeakEasy is an interactive web application designed to help users improve their spoken English skills using AI-powered speech recognition and text-to-speech technology.

## Features

### 🎯 Core Features
- **Speech Recognition**: Advanced AI analyzes your pronunciation and provides instant feedback
- **Text-to-Speech**: Listen to perfect pronunciation examples with native-like speech
- **Structured Lessons**: Progressive curriculum from beginner to advanced levels
- **Progress Tracking**: Monitor your improvement with detailed statistics and achievements
- **Free Practice Mode**: Practice with random phrases and get immediate feedback

### 📚 Learning Content
- **Beginner Level**: Basic greetings and common expressions
- **Intermediate Level**: Business English and complex sentences
- **Advanced Level**: Idiomatic expressions and challenging phrases
- **Pronunciation Scoring**: Real-time feedback on pronunciation accuracy
- **Interactive Lessons**: Step-by-step guided learning experience

### 🎨 User Experience
- **Modern UI**: Beautiful, responsive design that works on all devices
- **Real-time Feedback**: Instant pronunciation scoring and helpful tips
- **Progress Visualization**: Charts and statistics to track your learning journey
- **Achievement System**: Earn badges and celebrate your milestones

## Technologies Used

- **Backend**: Python Flask web framework
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Speech Recognition**: Web Speech API (browser-based)
- **Text-to-Speech**: Web Speech Synthesis API
- **Styling**: Custom CSS with responsive design
- **Icons**: Font Awesome 6

## Installation

### Prerequisites
- Python 3.7 or higher
- Modern web browser with microphone access
- Internet connection (for Font Awesome icons)

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   # If you have the files in a directory, navigate to it
   cd spoken-english-learning
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000` or `http://127.0.0.1:5000`

## Usage Guide

### Getting Started
1. **Allow Microphone Access**: When prompted, grant microphone permissions for speech recognition
2. **Choose Your Level**: Start with beginner lessons or jump to your appropriate level
3. **Practice Speaking**: Use the "Listen" button to hear examples, then record your pronunciation
4. **Track Progress**: Monitor your scores and achievements in the Progress section

### Features Overview

#### 🏠 Homepage
- Welcome message and feature overview
- Quick access to lessons and practice modes
- Attractive call-to-action buttons

#### 📖 Lessons Page
- Organized by difficulty level (Beginner, Intermediate, Advanced)
- Preview of phrases in each lesson
- Progress tracking for completed lessons

#### 🎓 Individual Lessons
- Step-by-step phrase practice
- Real-time pronunciation scoring
- Progress bar showing lesson completion
- Instant feedback and tips for improvement

#### 🏋️ Practice Mode
- Random phrase generation for free practice
- Session statistics and daily tracking
- Immediate feedback and scoring
- Practice tips and recommendations

#### 📊 Progress Tracking
- Overall statistics and achievements
- Detailed pronunciation scores
- Learning goals and recommendations
- Streak tracking and motivation

### Tips for Best Results
- **Quiet Environment**: Use the app in a quiet space for better speech recognition
- **Clear Speech**: Speak clearly and at a moderate pace
- **Regular Practice**: Aim for daily practice sessions to improve consistently
- **Listen First**: Always listen to the example before attempting to record
- **Be Patient**: Speech recognition may take a moment to process your audio

## Browser Compatibility

SpeakEasy works best with modern browsers that support the Web Speech API:

### ✅ Fully Supported
- **Google Chrome** (recommended)
- **Microsoft Edge**
- **Safari** (macOS/iOS)

### ⚠️ Limited Support
- **Firefox** (limited speech recognition support)
- **Opera** (depends on underlying engine)

### 📱 Mobile Support
- Works on mobile devices with supported browsers
- Touch-friendly interface
- Responsive design adapts to screen size

## Technical Details

### Architecture
- **MVC Pattern**: Clean separation of concerns
- **Session Management**: User progress stored in Flask sessions
- **RESTful APIs**: JSON-based communication for real-time updates
- **Progressive Enhancement**: Core functionality works without JavaScript

### Performance Features
- **Lazy Loading**: Resources loaded as needed
- **Efficient Algorithms**: Optimized pronunciation scoring
- **Local Storage**: Session data cached for better performance
- **Responsive Design**: Mobile-first approach

## Customization

### Adding New Lessons
Edit the `LESSONS` dictionary in `app.py` to add new content:

```python
'new_level': [
    {
        'id': 5,
        'title': 'Your Custom Lesson',
        'phrases': [
            {'text': 'Your phrase here', 'difficulty': 'easy'},
            # Add more phrases...
        ]
    }
]
```

### Styling Customization
Modify `static/css/style.css` to customize the appearance:
- Colors and themes
- Typography and fonts
- Layout and spacing
- Animations and effects

## Troubleshooting

### Common Issues

**Microphone Not Working**
- Ensure microphone permissions are granted
- Check browser microphone settings
- Verify microphone hardware functionality

**Speech Recognition Inaccurate**
- Speak more clearly and slowly
- Reduce background noise
- Try a different microphone
- Ensure stable internet connection

**Audio Playback Issues**
- Check browser audio settings
- Verify system volume levels
- Try refreshing the page
- Clear browser cache

**Performance Issues**
- Close unnecessary browser tabs
- Clear browser cache and data
- Restart the browser
- Check system resources

## Future Enhancements

### Planned Features
- **User Accounts**: Personal profiles and cloud sync
- **Advanced Analytics**: Detailed pronunciation analysis
- **Social Features**: Community learning and challenges
- **Offline Mode**: Download lessons for offline practice
- **Multi-language Support**: Additional language options
- **AI Tutor**: Personalized learning recommendations

### Contributing
This is a demonstration project, but suggestions for improvements are welcome!

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify browser compatibility
3. Ensure microphone permissions are granted
4. Try refreshing the page or restarting the browser

## License

This project is created for educational purposes and demonstrates modern web development techniques for language learning applications.

---

**Happy Learning! 🎉**

Start your journey to better English pronunciation with SpeakEasy today!