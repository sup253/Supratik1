// Practice-specific JavaScript

class PracticeManager {
    constructor() {
        this.currentPhrase = window.currentPhrase || { text: '', difficulty: 'easy' };
        this.speechManager = new SpeechRecognitionManager();
        this.ttsManager = new TextToSpeechManager();
        this.isRecording = false;
        
        this.sessionStats = {
            practiced: 0,
            scores: [],
            startTime: new Date()
        };
        
        this.initializeElements();
        this.setupEventListeners();
        this.loadSessionStats();
    }
    
    initializeElements() {
        this.elements = {
            practicePhrase: document.getElementById('practicePhrase'),
            getNewPhrase: document.getElementById('getNewPhrase'),
            playPhrase: document.getElementById('playPhrase'),
            practiceRecord: document.getElementById('practiceRecord'),
            practiceRecordText: document.getElementById('practiceRecordText'),
            practiceFeedback: document.getElementById('practiceFeedback'),
            practiceScore: document.getElementById('practiceScore'),
            feedbackTitle: document.getElementById('feedbackTitle'),
            feedbackMessage: document.getElementById('feedbackMessage'),
            feedbackTips: document.getElementById('feedbackTips'),
            totalPracticed: document.getElementById('totalPracticed'),
            averagePracticeScore: document.getElementById('averagePracticeScore'),
            practiceStreak: document.getElementById('practiceStreak')
        };
    }
    
    setupEventListeners() {
        this.elements.getNewPhrase.addEventListener('click', () => this.getNewPhrase());
        this.elements.playPhrase.addEventListener('click', () => this.playCurrentPhrase());
        this.elements.practiceRecord.addEventListener('click', () => this.toggleRecording());
    }
    
    loadSessionStats() {
        // Load stats from local storage for today
        const today = new Date().toDateString();
        const savedStats = Utils.loadFromStorage(`practice_stats_${today}`);
        
        if (savedStats) {
            this.sessionStats = { ...this.sessionStats, ...savedStats };
        }
        
        this.updateStatsDisplay();
    }
    
    saveSessionStats() {
        const today = new Date().toDateString();
        Utils.saveToStorage(`practice_stats_${today}`, {
            practiced: this.sessionStats.practiced,
            scores: this.sessionStats.scores
        });
    }
    
    updateStatsDisplay() {
        this.elements.totalPracticed.textContent = this.sessionStats.practiced;
        
        const averageScore = this.sessionStats.scores.length > 0
            ? this.sessionStats.scores.reduce((a, b) => a + b, 0) / this.sessionStats.scores.length
            : 0;
        
        this.elements.averagePracticeScore.textContent = Utils.formatScore(averageScore) + '%';
        
        // Calculate streak (simplified - just show days practiced this week)
        const daysThisWeek = this.calculatePracticeStreak();
        this.elements.practiceStreak.textContent = daysThisWeek;
    }
    
    calculatePracticeStreak() {
        let streak = 0;
        const today = new Date();
        
        for (let i = 0; i < 7; i++) {
            const checkDate = new Date(today);
            checkDate.setDate(today.getDate() - i);
            const dateStr = checkDate.toDateString();
            
            const dayStats = Utils.loadFromStorage(`practice_stats_${dateStr}`);
            if (dayStats && dayStats.practiced > 0) {
                streak++;
            } else if (i > 0) {
                break; // Break streak if no practice found
            }
        }
        
        return streak;
    }
    
    async getNewPhrase() {
        try {
            // In a real app, this would fetch from the server
            // For now, we'll simulate with a predefined list
            const samplePhrases = [
                { text: "How are you doing today?", difficulty: "easy" },
                { text: "I would like to make a reservation.", difficulty: "medium" },
                { text: "The weather is absolutely beautiful.", difficulty: "easy" },
                { text: "Could you please help me with this?", difficulty: "medium" },
                { text: "It's a piece of cake!", difficulty: "hard" },
                { text: "Actions speak louder than words.", difficulty: "hard" },
                { text: "Nice to meet you!", difficulty: "easy" },
                { text: "I'm looking forward to working with you.", difficulty: "medium" },
                { text: "That's the last straw!", difficulty: "hard" },
                { text: "Have a great day!", difficulty: "easy" }
            ];
            
            const randomPhrase = samplePhrases[Math.floor(Math.random() * samplePhrases.length)];
            this.currentPhrase = randomPhrase;
            
            this.updatePhraseDisplay();
            this.hideFeedback();
            
        } catch (error) {
            Utils.showNotification('Failed to get new phrase. Please try again.', 'error');
        }
    }
    
    updatePhraseDisplay() {
        this.elements.practicePhrase.textContent = this.currentPhrase.text;
        
        // Update difficulty badge
        const difficultyBadge = document.querySelector('.difficulty-badge');
        if (difficultyBadge) {
            difficultyBadge.textContent = this.currentPhrase.difficulty.charAt(0).toUpperCase() + 
                                        this.currentPhrase.difficulty.slice(1);
            difficultyBadge.className = `difficulty-badge difficulty-${this.currentPhrase.difficulty}`;
        }
    }
    
    playCurrentPhrase() {
        this.elements.playPhrase.disabled = true;
        
        this.ttsManager.speak(this.currentPhrase.text, {
            rate: 0.7,
            onStart: () => {
                this.elements.playPhrase.innerHTML = '<i class="fas fa-volume-up"></i> Playing...';
            },
            onEnd: () => {
                this.elements.playPhrase.disabled = false;
                this.elements.playPhrase.innerHTML = '<i class="fas fa-volume-up"></i> Listen';
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
        this.elements.practiceRecord.classList.add('recording');
        this.elements.practiceRecordText.textContent = 'Recording...';
        this.elements.practiceRecord.disabled = true;
        this.elements.playPhrase.disabled = true;
        
        this.speechManager.startRecording(
            (transcript, confidence) => {
                this.handleRecordingResult(transcript, confidence);
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
        this.elements.practiceRecord.classList.remove('recording');
        this.elements.practiceRecordText.textContent = 'Record';
        this.elements.practiceRecord.disabled = false;
        this.elements.playPhrase.disabled = false;
    }
    
    handleRecordingResult(transcript, confidence) {
        this.stopRecording();
        
        // Calculate pronunciation score
        const score = PronunciationScorer.calculateScore(
            this.currentPhrase.text, 
            transcript, 
            confidence
        );
        
        // Update session stats
        this.sessionStats.practiced++;
        this.sessionStats.scores.push(score);
        this.saveSessionStats();
        this.updateStatsDisplay();
        
        // Show feedback
        this.showFeedback(score, transcript);
        
        // Submit score to backend
        this.submitPronunciationScore(this.currentPhrase.text, score);
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
    
    showFeedback(score, transcript) {
        this.elements.practiceScore.textContent = Utils.formatScore(score);
        
        // Set feedback title based on score
        if (score >= 90) {
            this.elements.feedbackTitle.textContent = 'Excellent!';
            this.elements.feedbackTitle.style.color = '#28a745';
        } else if (score >= 80) {
            this.elements.feedbackTitle.textContent = 'Great Job!';
            this.elements.feedbackTitle.style.color = '#28a745';
        } else if (score >= 70) {
            this.elements.feedbackTitle.textContent = 'Good Work!';
            this.elements.feedbackTitle.style.color = '#ffc107';
        } else if (score >= 60) {
            this.elements.feedbackTitle.textContent = 'Keep Trying!';
            this.elements.feedbackTitle.style.color = '#ff7f00';
        } else {
            this.elements.feedbackTitle.textContent = 'Keep Practicing!';
            this.elements.feedbackTitle.style.color = '#dc3545';
        }
        
        // Set feedback message
        const feedbackMessage = PronunciationScorer.getFeedbackMessage(score);
        let message = feedbackMessage;
        
        if (transcript) {
            message += `<br><small style="font-style: italic;">You said: "${transcript}"</small>`;
        }
        
        this.elements.feedbackMessage.innerHTML = message;
        
        // Set tips based on score
        this.setFeedbackTips(score);
        
        this.elements.practiceFeedback.style.display = 'block';
        
        // Scroll to feedback
        this.elements.practiceFeedback.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    setFeedbackTips(score) {
        let tips = [];
        
        if (score < 60) {
            tips = [
                "Try speaking more slowly and clearly",
                "Make sure you're in a quiet environment",
                "Listen to the example again before recording",
                "Focus on pronouncing each word distinctly"
            ];
        } else if (score < 80) {
            tips = [
                "Work on stress patterns in sentences",
                "Pay attention to intonation",
                "Practice difficult sounds more"
            ];
        } else {
            tips = [
                "Excellent pronunciation!",
                "Try more challenging phrases",
                "Keep up the great work!"
            ];
        }
        
        this.elements.feedbackTips.innerHTML = tips.map(tip => 
            `<div style="margin: 0.25rem 0;"><i class="fas fa-lightbulb" style="color: #ffc107; margin-right: 0.5rem;"></i>${tip}</div>`
        ).join('');
    }
    
    hideFeedback() {
        this.elements.practiceFeedback.style.display = 'none';
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
}

// Initialize practice manager when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (window.currentPhrase) {
        window.practiceManager = new PracticeManager();
    }
});