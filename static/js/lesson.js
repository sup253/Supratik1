// Lesson-specific JavaScript

class LessonManager {
    constructor() {
        this.currentPhraseIndex = 0;
        this.phrases = window.lessonData.phrases || [];
        this.level = window.lessonData.level || 'beginner';
        this.lessonId = window.lessonData.lessonId || 1;
        this.scores = [];
        
        this.speechManager = new SpeechRecognitionManager();
        this.ttsManager = new TextToSpeechManager();
        
        this.isRecording = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.updateDisplay();
    }
    
    initializeElements() {
        this.elements = {
            phraseText: document.getElementById('phraseText'),
            phraseNumber: document.getElementById('phraseNumber'),
            phraseDifficulty: document.getElementById('phraseDifficulty'),
            listenBtn: document.getElementById('listenBtn'),
            recordBtn: document.getElementById('recordBtn'),
            nextBtn: document.getElementById('nextBtn'),
            recordText: document.getElementById('recordText'),
            progressFill: document.getElementById('lessonProgress'),
            progressText: document.getElementById('progressText'),
            recordingFeedback: document.getElementById('recordingFeedback'),
            pronunciationScore: document.getElementById('pronunciationScore'),
            feedbackText: document.getElementById('feedbackText'),
            lessonCompletion: document.getElementById('lessonCompletion'),
            averageScore: document.getElementById('averageScore'),
            phraseCard: document.getElementById('phraseCard')
        };
    }
    
    setupEventListeners() {
        this.elements.listenBtn.addEventListener('click', () => this.playCurrentPhrase());
        this.elements.recordBtn.addEventListener('click', () => this.toggleRecording());
        this.elements.nextBtn.addEventListener('click', () => this.nextPhrase());
    }
    
    updateDisplay() {
        const currentPhrase = this.phrases[this.currentPhraseIndex];
        if (!currentPhrase) return;
        
        // Update phrase content
        this.elements.phraseText.textContent = currentPhrase.text;
        this.elements.phraseNumber.textContent = this.currentPhraseIndex + 1;
        this.elements.phraseDifficulty.textContent = currentPhrase.difficulty;
        this.elements.phraseDifficulty.className = `difficulty-badge difficulty-${currentPhrase.difficulty}`;
        
        // Update progress
        const progressPercent = ((this.currentPhraseIndex) / this.phrases.length) * 100;
        this.elements.progressFill.style.width = progressPercent + '%';
        this.elements.progressText.textContent = `${this.currentPhraseIndex}/${this.phrases.length}`;
        
        // Reset UI state
        this.elements.recordingFeedback.style.display = 'none';
        this.elements.nextBtn.style.display = 'none';
        this.elements.recordBtn.disabled = false;
        this.elements.recordText.textContent = 'Start Recording';
    }
    
    playCurrentPhrase() {
        const currentPhrase = this.phrases[this.currentPhraseIndex];
        if (!currentPhrase) return;
        
        this.elements.listenBtn.disabled = true;
        
        this.ttsManager.speak(currentPhrase.text, {
            rate: 0.7,
            onStart: () => {
                this.elements.listenBtn.innerHTML = '<i class="fas fa-volume-up"></i> Playing...';
            },
            onEnd: () => {
                this.elements.listenBtn.disabled = false;
                this.elements.listenBtn.innerHTML = '<i class="fas fa-volume-up"></i> Listen';
            }
        });
    }
    
    toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            this.startRecording();
        }
    }
    
    startRecording() {
        if (this.isRecording) return;
        
        this.isRecording = true;
        this.elements.recordBtn.classList.add('recording');
        this.elements.recordText.textContent = 'Recording...';
        this.elements.recordBtn.disabled = true;
        this.elements.listenBtn.disabled = true;
        
        const currentPhrase = this.phrases[this.currentPhraseIndex];
        
        this.speechManager.startRecording(
            (transcript, confidence) => {
                this.handleRecordingResult(transcript, confidence, currentPhrase.text);
            },
            (error) => {
                this.handleRecordingError(error);
            }
        );
        
        // Auto-stop after 10 seconds
        setTimeout(() => {
            if (this.isRecording) {
                this.stopRecording();
            }
        }, 10000);
    }
    
    stopRecording() {
        this.isRecording = false;
        this.speechManager.stopRecording();
        this.elements.recordBtn.classList.remove('recording');
        this.elements.recordText.textContent = 'Try Again';
        this.elements.recordBtn.disabled = false;
        this.elements.listenBtn.disabled = false;
    }
    
    handleRecordingResult(transcript, confidence, expectedText) {
        this.stopRecording();
        
        // Calculate pronunciation score
        const score = PronunciationScorer.calculateScore(expectedText, transcript, confidence);
        this.scores.push(score);
        
        // Show feedback
        this.showFeedback(score, transcript, expectedText);
        
        // Submit score to backend
        this.submitPronunciationScore(expectedText, score);
        
        // Show next button
        this.elements.nextBtn.style.display = 'inline-flex';
    }
    
    handleRecordingError(error) {
        this.stopRecording();
        
        let errorMessage = 'Recording failed. Please try again.';
        
        if (error === 'not-allowed') {
            errorMessage = 'Microphone access denied. Please allow microphone access and try again.';
        } else if (error === 'no-speech') {
            errorMessage = 'No speech detected. Please speak louder and try again.';
        }
        
        Utils.showNotification(errorMessage, 'error');
    }
    
    showFeedback(score, transcript, expectedText) {
        this.elements.pronunciationScore.textContent = Utils.formatScore(score);
        
        const feedbackMessage = PronunciationScorer.getFeedbackMessage(score);
        const recognizedText = transcript ? `You said: "${transcript}"` : '';
        
        this.elements.feedbackText.innerHTML = `
            <p><strong>${feedbackMessage}</strong></p>
            ${recognizedText ? `<p style="margin-top: 0.5rem; font-style: italic;">${recognizedText}</p>` : ''}
        `;
        
        this.elements.recordingFeedback.style.display = 'block';
        
        // Add color coding based on score
        if (score >= 80) {
            this.elements.pronunciationScore.style.color = '#28a745';
        } else if (score >= 60) {
            this.elements.pronunciationScore.style.color = '#ffc107';
        } else {
            this.elements.pronunciationScore.style.color = '#dc3545';
        }
    }
    
    async submitPronunciationScore(phrase, score) {
        try {
            await Utils.makeAPICall('/api/submit_pronunciation', {
                phrase: phrase,
                score: score
            });
        } catch (error) {
            console.error('Failed to submit score:', error);
        }
    }
    
    nextPhrase() {
        this.currentPhraseIndex++;
        
        if (this.currentPhraseIndex >= this.phrases.length) {
            this.completeLesson();
        } else {
            this.updateDisplay();
            Utils.showNotification('Great! Moving to the next phrase.', 'success');
        }
    }
    
    async completeLesson() {
        // Calculate average score
        const averageScore = this.scores.length > 0 
            ? this.scores.reduce((a, b) => a + b, 0) / this.scores.length 
            : 0;
        
        // Update progress to 100%
        this.elements.progressFill.style.width = '100%';
        this.elements.progressText.textContent = `${this.phrases.length}/${this.phrases.length}`;
        
        // Hide phrase card and show completion
        this.elements.phraseCard.style.display = 'none';
        this.elements.lessonCompletion.style.display = 'block';
        this.elements.averageScore.textContent = Utils.formatScore(averageScore);
        
        // Submit lesson completion
        try {
            await Utils.makeAPICall('/api/complete_lesson', {
                lesson_id: this.lessonId,
                level: this.level
            });
            
            Utils.showNotification('Lesson completed successfully!', 'success');
        } catch (error) {
            console.error('Failed to submit lesson completion:', error);
        }
        
        // Scroll to completion section
        this.elements.lessonCompletion.scrollIntoView({ behavior: 'smooth' });
    }
}

// Initialize lesson when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (window.lessonData) {
        window.lessonManager = new LessonManager();
    }
});