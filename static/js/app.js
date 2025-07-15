// Main Application JavaScript

// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking nav links
        document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }));
    }
});

// Speech Recognition Setup
class SpeechRecognitionManager {
    constructor() {
        this.recognition = null;
        this.isSupported = false;
        this.isRecording = false;
        this.setupSpeechRecognition();
    }
    
    setupSpeechRecognition() {
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.isSupported = true;
        } else if ('SpeechRecognition' in window) {
            this.recognition = new SpeechRecognition();
            this.isSupported = true;
        }
        
        if (this.recognition) {
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
        }
    }
    
    startRecording(onResult, onError) {
        if (!this.isSupported) {
            onError('Speech recognition is not supported in this browser');
            return;
        }
        
        if (this.isRecording) {
            return;
        }
        
        this.isRecording = true;
        
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            const confidence = event.results[0][0].confidence;
            onResult(transcript, confidence);
        };
        
        this.recognition.onerror = (event) => {
            this.isRecording = false;
            onError(event.error);
        };
        
        this.recognition.onend = () => {
            this.isRecording = false;
        };
        
        this.recognition.start();
    }
    
    stopRecording() {
        if (this.recognition && this.isRecording) {
            this.recognition.stop();
            this.isRecording = false;
        }
    }
}

// Text-to-Speech Manager
class TextToSpeechManager {
    constructor() {
        this.synthesis = window.speechSynthesis;
        this.voices = [];
        this.loadVoices();
    }
    
    loadVoices() {
        this.voices = this.synthesis.getVoices();
        
        // If voices aren't loaded yet, wait for the event
        if (this.voices.length === 0) {
            this.synthesis.addEventListener('voiceschanged', () => {
                this.voices = this.synthesis.getVoices();
            });
        }
    }
    
    speak(text, options = {}) {
        // Cancel any ongoing speech
        this.synthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Set voice options
        utterance.rate = options.rate || 0.8;
        utterance.pitch = options.pitch || 1;
        utterance.volume = options.volume || 1;
        
        // Try to find an English voice
        const englishVoice = this.voices.find(voice => 
            voice.lang.startsWith('en') && !voice.name.includes('Google')
        );
        
        if (englishVoice) {
            utterance.voice = englishVoice;
        }
        
        // Event handlers
        if (options.onStart) {
            utterance.onstart = options.onStart;
        }
        
        if (options.onEnd) {
            utterance.onend = options.onEnd;
        }
        
        this.synthesis.speak(utterance);
    }
    
    stop() {
        this.synthesis.cancel();
    }
}

// Pronunciation Scoring (Basic Implementation)
class PronunciationScorer {
    static calculateScore(expected, actual, confidence) {
        if (!expected || !actual) return 0;
        
        // Convert to lowercase and clean
        const expectedClean = expected.toLowerCase().replace(/[^\w\s]/g, '');
        const actualClean = actual.toLowerCase().replace(/[^\w\s]/g, '');
        
        // Calculate similarity
        const similarity = this.calculateSimilarity(expectedClean, actualClean);
        
        // Factor in confidence from speech recognition
        const confidenceScore = confidence || 0.5;
        
        // Calculate final score (0-100)
        const baseScore = similarity * 80; // 80% based on text similarity
        const confidenceBonus = confidenceScore * 20; // 20% based on recognition confidence
        
        return Math.min(100, Math.round(baseScore + confidenceBonus));
    }
    
    static calculateSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;
        
        if (longer.length === 0) return 1.0;
        
        return (longer.length - this.editDistance(longer, shorter)) / longer.length;
    }
    
    static editDistance(str1, str2) {
        const matrix = [];
        
        for (let i = 0; i <= str2.length; i++) {
            matrix[i] = [i];
        }
        
        for (let j = 0; j <= str1.length; j++) {
            matrix[0][j] = j;
        }
        
        for (let i = 1; i <= str2.length; i++) {
            for (let j = 1; j <= str1.length; j++) {
                if (str2.charAt(i - 1) === str1.charAt(j - 1)) {
                    matrix[i][j] = matrix[i - 1][j - 1];
                } else {
                    matrix[i][j] = Math.min(
                        matrix[i - 1][j - 1] + 1,
                        matrix[i][j - 1] + 1,
                        matrix[i - 1][j] + 1
                    );
                }
            }
        }
        
        return matrix[str2.length][str1.length];
    }
    
    static getFeedbackMessage(score) {
        if (score >= 90) {
            return "Excellent pronunciation! You sound like a native speaker.";
        } else if (score >= 80) {
            return "Great job! Your pronunciation is very clear.";
        } else if (score >= 70) {
            return "Good work! Keep practicing to improve further.";
        } else if (score >= 60) {
            return "Not bad! Focus on clarity and try again.";
        } else {
            return "Keep practicing! Try speaking more slowly and clearly.";
        }
    }
}

// Utility Functions
const Utils = {
    // API call helper
    async makeAPICall(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    },
    
    // Show notification
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '1rem 1.5rem',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '600',
            zIndex: '9999',
            transform: 'translateX(100%)',
            transition: 'transform 0.3s ease'
        });
        
        // Set background color based on type
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#17a2b8'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    },
    
    // Format score for display
    formatScore(score) {
        return Math.round(score);
    },
    
    // Local storage helpers
    saveToStorage(key, data) {
        localStorage.setItem(key, JSON.stringify(data));
    },
    
    loadFromStorage(key) {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    }
};

// Make classes globally available
window.SpeechRecognitionManager = SpeechRecognitionManager;
window.TextToSpeechManager = TextToSpeechManager;
window.PronunciationScorer = PronunciationScorer;
window.Utils = Utils;