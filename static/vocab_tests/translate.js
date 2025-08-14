const api = `http://127.0.0.1:8000`;
const sessionSize = 10;
let currentIndex = 0;
let words = [];

let userAnswer = ''

const sendBtn = document.querySelector('#send');
const nextSessionContainer = document.querySelector('.next-session-button');
const wordDisplay = document.querySelector('.word-display');
const options = document.querySelector('.options');
const infoBlock = document.querySelector('.info-block');
const quizContainer = document.querySelector(".options");

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
    quizContainer.innerHTML = '';

    if (words.length === 0) {
        wordDisplay.textContent = 'Congratulations';
        sendBtn.style.display = 'none';
        infoBlock.style.display = 'inline-block';
        return;
    }

    if (currentIndex >= sessionSize || currentIndex >= words.length) {
        wordDisplay.textContent = 'Session finished 🎉';
        sendBtn.style.display = 'none';
        nextSessionContainer.style.display = 'inline-block';
        return;
    }

    const word = words[currentIndex];
    wordDisplay.textContent = word.question || '';

    word.options.forEach(async element => {

        const btn = document.createElement("button");
        btn.classList.add('options_btn')
        btn.textContent = element;


        btn.addEventListener("click", async () => {

            const buttons = document.querySelectorAll("#quiz button");

            document.querySelectorAll('#quiz button').forEach(button => {
                button.disabled = true;
            });

            const data = {
                user_answer: element,
                word_id: word.word_id
            };

            const correctWord = await sendWord(data, `${api}/api/test?test_type=translate_ru`);
            if (element === correctWord) {
                btn.style.backgroundColor = "lightgreen";
            } else {
                btn.style.backgroundColor = "lightcoral";
                buttons.forEach(b => {
                    if (b.textContent.trim() === correctWord.trim()) {
                        b.style.backgroundColor = "lightgreen";
                    }
                });
            }
            sendBtn.style.display = 'inline-block'
        });

        quizContainer.appendChild(btn);
    });
}

sendBtn.addEventListener('click', () => {
    sendBtn.style.display = 'none';
    currentIndex++;
    showWord();
});

nextSessionContainer.addEventListener('click', async () => {
    words = await getArray(`${api}/api/translate`);
    currentIndex = 0;
    nextSessionContainer.style.display = 'none';
    showWord();
});

async function start() {
    words = await getArray(`${api}/api/translate`);
    showWord();
}

start();
