const api = `http://127.0.0.1:8000`;
const sessionSize = 10;
let currentIndex = 0;
let words = [];

// селекторы под новые классы
const wordInput = document.querySelector('.word-input');
const checkBtn = document.querySelector('#check');
const sendBtn = document.querySelector('#send');
const nextSessionContainer = document.querySelector('.next-session-button');
const wordDisplay = document.querySelector('.word-display');
const spell = document.querySelector('.spell');
const infoBlock = document.querySelector('.info-block');

// создаём блоки с ошибкой и ответами
const error = document.createElement("div");
error.classList.add('error');
spell.append(error);

const showAnswer = document.createElement("div");
showAnswer.classList.add('show-answer');

const correctAnswer = document.createElement("div");
correctAnswer.classList.add('correct-answer');

const userAnswer = document.createElement("div");
userAnswer.classList.add('user-answer');

showAnswer.append(correctAnswer);
showAnswer.append(userAnswer);
spell.append(showAnswer);

async function getArray(url) {
    const response = await fetch(url);
    const array = await response.json();
    return array;
}

function sendWord(data, url) {
    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
}

function showWord() {
    if (words.length === 0) {
        wordDisplay.textContent = 'Congratulations';
        wordInput.style.display = 'none';
        checkBtn.style.display = 'none';
        sendBtn.style.display = 'none';
        infoBlock.style.display = 'inline-block';
        return;
    }

    if (currentIndex >= sessionSize || currentIndex >= words.length) {
        wordDisplay.textContent = 'Session finished 🎉';
        wordInput.style.display = 'none';
        checkBtn.style.display = 'none';
        sendBtn.style.display = 'none';
        nextSessionContainer.style.display = 'inline-block';
        return;
    }

    const word = words[currentIndex];
    wordDisplay.textContent = word.translate_ru || '';
    wordInput.value = '';
}

nextSessionContainer.addEventListener('click', async () => {
    words = await getArray(`${api}/api/to_learn?test_type=spelling`);

    currentIndex = 0;
    wordInput.style.display = 'inline-block';
    checkBtn.style.display = 'inline-block';
    nextSessionContainer.style.display = 'none';
    showWord();
});

checkBtn.addEventListener('click', () => {
    const answer = wordInput.value.trim();
    const wordData = words[currentIndex];

    const data = {
        answer: answer,
        id: wordData.id
    };

    if (!answer) {
        error.textContent = `Write answer maaaan!!!`;
        return;
    }

    error.textContent = '';

    if (answer !== wordData.word) {
        wordInput.style.display = 'none';
        correctAnswer.textContent = wordData.word;
        userAnswer.textContent = answer;
    } else {
        wordInput.style.display = 'none';
        correctAnswer.textContent = answer;
        sendWord(data, `${api}/api/test?test_type=spelling`);
    }

    sendBtn.style.display = 'inline-block';
    checkBtn.style.display = 'none';
});

sendBtn.addEventListener('click', () => {
    correctAnswer.textContent = '';
    userAnswer.textContent = '';
    checkBtn.style.display = 'inline-block';
    sendBtn.style.display = 'none';
    wordInput.style.display = 'inline-block';

    currentIndex++;
    showWord();
});

async function start() {
    words = await getArray(`${api}/api/to_learn?test_type=spelling`);
    showWord();
}

start();
