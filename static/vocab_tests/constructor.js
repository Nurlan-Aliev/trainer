const api = `http://127.0.0.1:8000`;
const sessionSize = 10;
let currentIndex = 0;
let words = [];


const wordInput = document.querySelector('.word-input');
const checkBtn = document.querySelector('#check');
const sendBtn = document.querySelector('#send');
const nextSessionContainer = document.querySelector('.next-session-button');
const wordDisplay = document.querySelector('.word-display');
const spell = document.querySelector('.spell');
const infoBlock = document.querySelector('.info-block');


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

async function sendWord(data, url) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    const correct_answer = await response.json();
    return correct_answer
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
    wordDisplay.textContent = word.word_ru || '';
    wordInput.value = '';
}

nextSessionContainer.addEventListener('click', async () => {
    words = await getArray(`${api}/api/constructor`);

    currentIndex = 0;
    wordInput.style.display = 'inline-block';
    checkBtn.style.display = 'inline-block';
    nextSessionContainer.style.display = 'none';
    showWord();
});

checkBtn.addEventListener('click', async () => {
    const answer = wordInput.value.trim();
    const wordData = words[currentIndex];
    
    if (!answer) {
        error.textContent = `Write answer maaaan!!!`;
        return;
    }
    error.textContent = ``;

    const data = {
        user_answer: answer,
        word_id: wordData.word_id
    };

    const correct_answer = await sendWord(data, `${api}/api/test?test_type=spelling`);

    if (answer !== correct_answer) {

        wordInput.style.display = 'none';
        correctAnswer.textContent = correct_answer;
        userAnswer.textContent = answer;
    } else {

        wordInput.style.display = 'none';
        correctAnswer.textContent = correct_answer;
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
    words = await getArray(`${api}/api/constructor`);
    showWord();
}

start();
