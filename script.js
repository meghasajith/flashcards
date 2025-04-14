document.addEventListener('DOMContentLoaded', function () {
    let currentCardIndex = 0;
    const flashcards = document.querySelectorAll('.flashcard');
    const totalCards = flashcards.length;
    let correctCount = 0;
    let incorrectCount = 0;

    // Initialize progress bar
    updateProgress();

    // Add keyboard controls
    document.addEventListener('keydown', function(e) {
        switch(e.key) {
            case ' ':  // Spacebar
            case 'Enter':
                flipCurrentCard();
                break;
            case 'ArrowRight':
            case 'n':
                nextCard();
                break;
            case 'ArrowLeft':
            case 'p':
                previousCard();
                break;
            case '1':
                markCard(true);
                break;
            case '0':
                markCard(false);
                break;
        }
    });

    // Add click listeners to all flashcards
    flashcards.forEach((card, index) => {
        card.addEventListener('click', () => {
            card.classList.toggle('flipped');
        });
    });

    function flipCurrentCard() {
        if (flashcards[currentCardIndex]) {
            flashcards[currentCardIndex].classList.toggle('flipped');
        }
    }

    function nextCard() {
        if (currentCardIndex < totalCards - 1) {
            flashcards[currentCardIndex].classList.remove('flipped');
            flashcards[currentCardIndex].style.display = 'none';
            currentCardIndex++;
            flashcards[currentCardIndex].style.display = 'block';
            updateProgress();
        }
    }

    function previousCard() {
        if (currentCardIndex > 0) {
            flashcards[currentCardIndex].classList.remove('flipped');
            flashcards[currentCardIndex].style.display = 'none';
            currentCardIndex--;
            flashcards[currentCardIndex].style.display = 'block';
            updateProgress();
        }
    }

    function markCard(isCorrect) {
        if (isCorrect) {
            correctCount++;
            flashcards[currentCardIndex].classList.add('correct');
        } else {
            incorrectCount++;
            flashcards[currentCardIndex].classList.add('incorrect');
        }
        updateStats();
        setTimeout(nextCard, 500);
    }

    function updateProgress() {
        const progressBar = document.querySelector('.progress-bar-fill');
        if (progressBar) {
            const progress = ((currentCardIndex + 1) / totalCards) * 100;
            progressBar.style.width = `${progress}%`;
        }
    }

    function updateStats() {
        const correctElement = document.querySelector('.correct-count');
        const incorrectElement = document.querySelector('.incorrect-count');
        
        if (correctElement) {
            correctElement.textContent = correctCount;
        }
        if (incorrectElement) {
            incorrectElement.textContent = incorrectCount;
        }
    }

    // Initialize display
    if (totalCards > 0) {
        flashcards.forEach((card, index) => {
            card.style.display = index === 0 ? 'block' : 'none';
        });
    }
});

function toggleAnswer() {
    const answer = document.getElementById("answer");
    if (answer.style.display === "none") {
        answer.style.display = "block";
    } else {
        answer.style.display = "none";
    }
}
