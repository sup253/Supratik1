// Common JavaScript functionality for English Skills Improver

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Add loading spinner functionality
function showLoadingSpinner(element) {
    const originalText = element.innerHTML;
    element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    element.disabled = true;
    
    return function() {
        element.innerHTML = originalText;
        element.disabled = false;
    };
}

// Toast notification system
function showToast(message, type = 'info') {
    // Remove existing toast if any
    const existingToast = document.querySelector('.custom-toast');
    if (existingToast) {
        existingToast.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = `custom-toast alert alert-${type} position-fixed`;
    toast.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 1050;
        min-width: 300px;
        animation: slideInRight 0.3s ease-out;
    `;
    toast.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <span>${message}</span>
            <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }
    }, 5000);
}

// Add CSS animations for toast
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .custom-toast {
        border: none;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
`;
document.head.appendChild(style);

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + H for Home
    if ((e.ctrlKey || e.metaKey) && e.key === 'h') {
        e.preventDefault();
        window.location.href = '/';
    }
    
    // Ctrl/Cmd + V for Vocabulary
    if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
        e.preventDefault();
        window.location.href = '/vocabulary';
    }
    
    // Ctrl/Cmd + G for Grammar
    if ((e.ctrlKey || e.metaKey) && e.key === 'g') {
        e.preventDefault();
        window.location.href = '/grammar';
    }
    
    // Ctrl/Cmd + R for Reading (only if not on reading page to avoid conflict with refresh)
    if ((e.ctrlKey || e.metaKey) && e.key === 'r' && !window.location.pathname.includes('/reading')) {
        e.preventDefault();
        window.location.href = '/reading';
    }
    
    // Ctrl/Cmd + W for Writing
    if ((e.ctrlKey || e.metaKey) && e.key === 'w') {
        e.preventDefault();
        window.location.href = '/writing';
    }
});

// Progress tracking
function updateProgress(section, score) {
    const progress = JSON.parse(localStorage.getItem('englishProgress') || '{}');
    
    if (!progress[section]) {
        progress[section] = [];
    }
    
    progress[section].push({
        score: score,
        date: new Date().toISOString(),
        timestamp: Date.now()
    });
    
    // Keep only last 10 attempts per section
    progress[section] = progress[section].slice(-10);
    
    localStorage.setItem('englishProgress', JSON.stringify(progress));
}

// Get progress statistics
function getProgressStats(section) {
    const progress = JSON.parse(localStorage.getItem('englishProgress') || '{}');
    
    if (!progress[section] || progress[section].length === 0) {
        return {
            attempts: 0,
            averageScore: 0,
            lastScore: 0,
            improvement: 0
        };
    }
    
    const scores = progress[section].map(p => p.score);
    const attempts = scores.length;
    const averageScore = scores.reduce((a, b) => a + b, 0) / attempts;
    const lastScore = scores[scores.length - 1];
    const firstScore = scores[0];
    const improvement = attempts > 1 ? lastScore - firstScore : 0;
    
    return {
        attempts,
        averageScore: Math.round(averageScore),
        lastScore,
        improvement: Math.round(improvement)
    };
}

// Theme toggle functionality (for future enhancement)
function toggleTheme() {
    const body = document.body;
    const isDark = body.classList.toggle('dark-theme');
    localStorage.setItem('darkTheme', isDark);
}

// Load saved theme preference
document.addEventListener('DOMContentLoaded', function() {
    const isDark = localStorage.getItem('darkTheme') === 'true';
    if (isDark) {
        document.body.classList.add('dark-theme');
    }
    
    // Add keyboard shortcut hints to tooltips
    const keyboardHints = document.createElement('div');
    keyboardHints.className = 'keyboard-hints position-fixed';
    keyboardHints.style.cssText = `
        bottom: 20px;
        left: 20px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        display: none;
        z-index: 1000;
    `;
    keyboardHints.innerHTML = `
        <strong>Keyboard Shortcuts:</strong><br>
        Ctrl+H: Home | Ctrl+V: Vocabulary<br>
        Ctrl+G: Grammar | Ctrl+W: Writing
    `;
    document.body.appendChild(keyboardHints);
    
    // Show hints on Ctrl key hold
    let ctrlPressed = false;
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && !ctrlPressed) {
            ctrlPressed = true;
            keyboardHints.style.display = 'block';
        }
    });
    
    document.addEventListener('keyup', function(e) {
        if (!e.ctrlKey && ctrlPressed) {
            ctrlPressed = false;
            keyboardHints.style.display = 'none';
        }
    });
});

// Performance tracking
function trackTime(activity) {
    const startTime = Date.now();
    
    return function() {
        const endTime = Date.now();
        const duration = endTime - startTime;
        
        const timeTracking = JSON.parse(localStorage.getItem('englishTimeTracking') || '{}');
        
        if (!timeTracking[activity]) {
            timeTracking[activity] = [];
        }
        
        timeTracking[activity].push({
            duration: duration,
            date: new Date().toISOString()
        });
        
        // Keep only last 50 sessions per activity
        timeTracking[activity] = timeTracking[activity].slice(-50);
        
        localStorage.setItem('englishTimeTracking', JSON.stringify(timeTracking));
        
        return duration;
    };
}