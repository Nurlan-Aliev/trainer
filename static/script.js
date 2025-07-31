async function getArray(url) {
  const response = await fetch(url);
  const array = await response.json();
  return array;
}

const sessionSize = 10;
let count         = 0
let currentIndex  = 0;
let words         = [];

const statsEl   = document.getElementById('stats');
const wordEl    = document.getElementById('word');
const transEl   = document.getElementById('trans');
const knowBtn   = document.querySelector('.i_know');
const learnBtn  = document.querySelector('.to_learn');
const nextSession  = document.querySelector('.next-session');


function showWord() {
  if (currentIndex >= sessionSize || currentIndex >= words.length) {
    wordEl.textContent = 'Session finished 🎉';
    knowBtn.style.display = 'none';
    learnBtn.style.display = 'none';
    nextSession.style.display = 'inline-block';
    return;
  }

  const word = words[currentIndex];
  wordEl.textContent = word.word;
  transEl.textContent = word.translate_ru ? word.translate_ru: ' ' ;
}

nextSession.addEventListener('click', async() =>  {
  count = count + 10
  words = await getArray(`http://127.0.0.1:8000/api/?skip=${count}`)
  currentIndex = 0;
  knowBtn.style.display = 'inline-block';
  learnBtn.style.display = 'inline-block';
  nextSession.style.display = 'none'
  showWord();
}
)

knowBtn.addEventListener('click', () => {
  let word = words[currentIndex];
  fetch(`http://127.0.0.1:8000/api/learned`, {
  method: "POST", 
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(word)
})
  currentIndex++;
  showWord();
});


learnBtn.addEventListener('click', () => {
  currentIndex++;
  showWord();
});

async function start() {
  words = await getArray(`http://127.0.0.1:8000/api/?skip=${count}`);
  showWord();
}

start();
