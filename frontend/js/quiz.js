let questions = [];
let currentQuestion = 0;
let score = 0;
let startTime;
let timerInterval;
let timeRemaining;
let currentMode;
let currentDifficulty;

const timer_durations = {
    note_reading: {
        bronze: 195,
        silver: 150,
        gold:  105,
        maestro: 90,
     },
    scales: {
        bronze: 525,
        silver: 450,
        gold: 375,
        maestro: 225,
    },
    chord_analysis: {
        bronze: 750,
        silver: 600,
        gold: 525,
        maestro: 450,
    },
}

function generateNotePool() {
    const naturals = ['C', 'D', 'E', 'F', 'G', 'A', 'B'];
    const accidentals = ['#', 'b'];
    let pool = [];

    pool.push(...naturals);

    for (const note of naturals) {
        for (const acc of accidentals) {
            pool.push(note + acc);
        }
    }
    return pool;
}

function generateScalePool() {
    const tonics = ["Ab", "A", "Bb", "B", "C",  "Db", "D", "Eb", "E", "F", "F#", "Gb", "G",];
    const types = [
        'Major_scale', 
        'Natural_minor', 
        'Harmonic_minor', 
        'Melodic_minor',
        'Dorian', 
        'Phrygian', 
        'Lydian', 
        'Mixolydian', 
        'Locrian'
    ];

    const pool = [];
    for (const tonic of tonics) {
        for (const type of types) {
            pool.push(`${tonic} ${type}`);
        }
    }
    return pool;
}

function generateChordPool() {
    const roots = ["Ab", "A", "Bb", "B", "C",  "Db", "D", "Eb", "E", "F", "F#", "Gb", "G",];
    const qualities = ['Major', 'Minor', 'Dim7', 'Augmented', 'Diminished', 'Dominant7', 'Minor7', 'Major7', 'HalfDim7',];
    
    const pool = [];
    for (const root of roots) {
        for (const quality of qualities) {
            pool.push(`${root} ${quality}`);
        }
    }
    return pool;
}

const answer_pool = {
    note_reading: generateNotePool(),
    scales: generateScalePool(),
    chord_analysis: generateChordPool(),
};

//Initialize the quiz
async function loadQuiz() {

    const uriParams = new URLSearchParams(window.location.search);
    currentMode = (uriParams.get('mode') || 'note_reading').toLowerCase();

    const questionImage = document.getElementById('question-image');

    if (currentMode === 'scales') {
        questionImage.classList.add('multi-measure');
        questionImage.classList.remove('single-measure');
    } else {
        questionImage.classList.add('single-measure');
        questionImage.classList.remove('multi-measure');
    }

    if(!currentMode) {
        alert("No mode selected! Redirecting to mode selection.");
        window.location.href = 'selection.html';
        return;
    }
    
    const modeTitle = currentMode.replace('_', ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    document.getElementById('mode-title').textContent = modeTitle;

    currentDifficulty = 'bronze'; //Default difficulty for now until further implemented

    timeRemaining = timer_durations[currentMode][currentDifficulty];
    document.getElementById('timer').textContent = timeRemaining;

      try {
        const response = await fetch(`http://localhost:5000/${currentMode}/${currentDifficulty}`);
        
        if (!response.ok) {
            throw new Error('Failed to load questions');
        }
        
        let allQuestions = await response.json();

        questions = allQuestions.sort(() => Math.random() - 0.5).slice(0, 15);
        
        // Generate answer options for each question
        questions = questions.map(q => ({
            ...q,
            options: generateOptions(q.answer, currentMode)
        }));
        
        
        document.getElementById('total-questions').textContent = questions.length;
        document.getElementById('current-question').textContent = '1';
        document.getElementById('score').textContent = '0';
        
       
        startTime = Date.now();
        startTimer();
        displayQuestion();
        
    } catch (error) {
        console.error('Error loading quiz:', error);
        alert('Failed to load questions. Please try again.');
        window.location.href = 'selection.html';
    }
}

let quizFinished = false;
let quizStarted = true;

function startTimer() {
    timerInterval = setInterval(() => {
        if (quizFinished) return;
        timeRemaining--;
        document.getElementById('timer').textContent = timeRemaining;
        
        if (timeRemaining <= 0) {
            quizFinished = true;
            clearInterval(timerInterval);
            handleTimeout();
        }
    }, 1000);
}



// Display questions
function displayQuestion() {
    const q = questions[currentQuestion];
    document.getElementById('question-image').src = q.image;
    document.getElementById('question-image').alt = q.question;
    document.getElementById('current-question').textContent = currentQuestion + 1;
    
    // Update answer buttons 
    const buttons = document.querySelectorAll('.answer-btn');
    buttons.forEach((btn, index) => {
        btn.textContent = q.options[index];
        btn.disabled = false;
        btn.className = 'answer-btn';
    });
}

function checkAnswer(buttonIndex) {
    const q = questions[currentQuestion];
    const buttons = document.querySelectorAll('.answer-btn');
    const selectedAnswer = q.options[buttonIndex];
    
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.classList.add('disabled');
    });
    
    if (selectedAnswer === q.answer) {
        score++;
        buttons[buttonIndex].classList.add('correct');
        document.getElementById('score').textContent = score;
    } else {
        buttons[buttonIndex].classList.add('wrong');
        
        buttons.forEach((btn, i) => {
            if (q.options[i] === q.answer) {
                btn.classList.add('correct');
            }
        });
    }

    setTimeout(async () => {
        currentQuestion++;
        
        if (currentQuestion < questions.length) {
            displayQuestion();
        } else {
             handleCompletion();
        }
    }, 1500);
}

// Enable buttons at start & ensures they won't submit pls pls pls work
const buttons = document.querySelectorAll('.answer-btn');
buttons.forEach(btn => {
    btn.type = 'button'; 
    btn.disabled = false;
});


 function handleCompletion() {
    if (quizFinished) return;
    quizFinished = true;
    clearInterval(timerInterval);

    let username = localStorage.getItem('user');

    if (!username) {
        username = prompt('Enter a name for the leaderboard:');
        if (username && username.trim()) {
            username = username.trim();
            localStorage.setItem('user', username);
        } else {
            username = 'Anonymous';
        }
    }
    
    const timeTaken = Math.round((Date.now() - startTime) / 1000);
    const accuracy = Math.round((score / questions.length) * 100);
    const rr = Math.round(accuracy * 60 / (timeTaken + 1));
    
    document.getElementById('final-accuracy').textContent = `${accuracy}%`;
    document.getElementById('final-time').textContent = `${timeTaken}s`;
    document.getElementById('final-rr').textContent = rr;
    
    submitScore(accuracy, timeTaken);
    document.getElementById('completion-modal').classList.remove('modal-hidden');
}


// Ran out of time
function handleTimeout() {
    if (quizFinished) return;
    quizFinished = true;
    clearInterval
    const timeTaken = timer_durations[currentMode][currentDifficulty];
    const questionsAnswered = currentQuestion;
    const accuracy = questionsAnswered > 0 ? Math.round((score / questionsAnswered) * 100) : 0;
    const rr = Math.round(accuracy * 60 / (timeTaken + 1));
    
    document.getElementById('timeout-questions').textContent = `${questionsAnswered}/${questions.length}`;
    document.getElementById('timeout-accuracy').textContent = `${accuracy}%`;
    document.getElementById('timeout-rr').textContent = rr;

  submitScore(accuracy, timeTaken);
    
    document.getElementById('timeout-modal').classList.remove('modal-hidden');
}

//IT FINALLY WORKED YESSSS!!!!!
function submitScore(username, accuracy, timeTaken) { 
    fetch('http://localhost:5000/submit_score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user: username,
            accuracy: accuracy,
            time_taken: timeTaken,
            mode: currentMode,
            difficulty: currentDifficulty
        })
    })
    .then(res => res.json().catch(() => ({})))
    .then(result => {
        if (!result || result.error) {
            console.warn('Score submission failed:', result.error || 'Unknown error');
            if (result && result.error && result.error.includes('famous musician')) {
                alert(result.error + " Please choose a different name for your next session.");
                localStorage.removeItem('user');
            }
        } else {
            console.log('Score submitted successfully:', result);
        }
    })
    .catch(err => {
        console.error("Score submission failed:", err);
    });
}


function generateOptions(correctAnswer, mode) {
    const pool = answer_pool[mode] || [];
    
    const wrongAnswers = pool
        .filter(answer => answer !== correctAnswer)
        .sort(() => Math.random() - 0.5)
        .slice(0, 3);
    
    while (wrongAnswers.length < 3) {
        wrongAnswers.push(`Option ${wrongAnswers.length + 1}`);
    }
    
    // shuffle answers
    const options = [correctAnswer, ...wrongAnswers]
        .sort(() => Math.random() - 0.5);
    
    return options;
}

document.addEventListener('DOMContentLoaded', loadQuiz); 