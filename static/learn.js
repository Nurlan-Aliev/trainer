const sessionSize = 10;
let count         = 0
let currentIndex  = 0;
let words         = [];

const statsEl   = document.querySelector('#stats');
const wordEl    = document.querySelector('#word');
const transEl   = document.querySelector('#trans');
const knowBtn   = document.querySelector('.i_know');
const learnBtn  = document.querySelector('.to_learn');
const nextSession  = document.querySelector('.next-session');


async function getArray(url) {
  const response = await fetch(url);
  const array = await response.json();
  return array;
}


function sendWord(word, url){
  fetch(url, {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(word)
})}



function showWord() {
  if (currentIndex >= sessionSize || currentIndex >= words.length) {
    wordEl.textContent = 'Session finished 🎉';
    knowBtn.style.display = 'none';
    learnBtn.style.display = 'none';
    nextSession.style.display = 'inline-block';
    return;
  }

  const word = words[currentIndex];
  wordEl.textContent = word.word_en;
  transEl.textContent = word.word_ru ? word.word_ru: ' ' ;
}

nextSession.addEventListener('click', async() =>  {
  count = count + 10
  words = await getArray(`${api}/api/?skip=${count}`)
  currentIndex = 0;
  knowBtn.style.display = 'inline-block';
  learnBtn.style.display = 'inline-block';
  nextSession.style.display = 'none'
  showWord();
}
)

knowBtn.addEventListener('click', () => {
  sendWord(words[currentIndex], `${api}/api/learned`)
  currentIndex++;
  showWord();
});


learnBtn.addEventListener('click', () => {
  sendWord(words[currentIndex], `${api}/api/to_learn`)
  currentIndex++;
  showWord();
});

async function start() {
  words = await getArray(`${api}/api/?skip=${count}`);
  showWord();
}

start();
