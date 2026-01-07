# Trainer — Language Learning Platform (Backend)

Backend service for a language learning platform focused on vocabulary acquisition using test-based repetition.  
The system tracks user progress and considers a word **learned** after successfully passing **four different tests**.

---

## Features

- JWT-based authentication with **access and refresh tokens**
- Token invalidation using **Redis**
- REST API built with **FastAPI**
- Asynchronous database access with **SQLAlchemy**
- Vocabulary learning workflow with **test-based progression**
- Admin endpoints for managing words
- Dockerized infrastructure with **Docker Compose**
- **Nginx** as a reverse proxy and unified entry point

---

## Tech Stack

- **Backend:** FastAPI  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy (async)  
- **Authentication:** JWT (access & refresh tokens)  
- **Cache:** Redis  
- **DevOps:** Docker, Docker Compose, Nginx  
- **Frontend:** Vue.js (separate repository)

---

## Learning Logic Overview

- The platform contains a preloaded vocabulary of approximately **3000 English words**
- A user can mark a word as:
  - **Known**
  - **To learn**
- Words marked as **to learn** are added to a testing workflow
- A word is considered **learned** only after passing **4 tests**:
  1. Translation test (native language → English, multiple choice)
  2. Reverse translation test (English → native language, multiple choice)
  3. Typing test (user types the word manually)
  4. Remember / Forgot test (honesty-based confirmation)

After successfully passing all tests:
- the word is moved from `words_to_learn` to `learned_words`
- test history is cleared

---

## Authentication Flow

- Authentication is implemented using **JWT**
- **Access token lifetime:** ~4 minutes
- **Refresh token lifetime:** ~10080 minutes (7 days)
- Refresh tokens are invalidated and stored in **Redis** on logout or early expiration
- Redis acts as a **blacklist** for invalid refresh tokens

---

## Database Schema (Simplified)

Main tables:
- users
- words
- words_to_learn
- learned_words
- user_word_test_results

---

## API Overview

### Authentication
- POST `/auth/login`
- POST `/auth/refresh`
- POST `/auth/logout`
- GET `/auth/me`

### Vocabulary

---
- GET `/api/` => 
  - Response
  ```
  list[
    dict[
      'id': int,
      'word_en': str,
      'word_ru': str,
      'word_az': str
    ]
  ] 
  ```
---

- POST `/api/to_learn` =>
  
  - Request body
  ```
  {
    'id': int,
    'word_en': str,
    'word_ru': str,
    'word_az': str
  } 
  ```
  - Response
  ```
  {
    None
  }
  ```
---
- GET `/api/learned`=>
  
  - Request body
  ```
  {
    'id': int,
    'word_en': str,
    'word_ru': str,
    'word_az': str
  } 
  ```
  - Response
  ```
  {
    None
  }
  ```
---
- GET `/api/learned_word_count`=>
  - Response
  ```
  {
    int
  }
  ```
--- 

### Tests
- GET `/api/constructor` => 
  - Response
  ```
  list[
    {
      'id': int,
      'word_ru': str,
      'word_az': str
    }
  ] 
  ```
- GET `/api/translate` => 
  - Response
  ```
  list[
    {
      word_id: int
      question: {
        'word_ru': word_ru,
        'word_az': word_az
      }
      options: list[
        {'word_en': word_en} * 4
        ]
    } * 10
  ] 
  ```
  
- GET `/api/rev_translate` => 
  - Response
  ```
  list[
    {
      word_id: int
      question: {'word_en': word_en }
      options: list[{'word_ru': word.word_ru, 'word_az': word.word_az} *4 ]
    } * 10
  ]
  ```
- GET `/api/remember` => 
  - Response
  ```
  list[
    {
      'id': int,
      'word_en': str,
      'word_ru': str,
      'word_az': str
    }
  ] 
  ```
---

- POST `/api/constructor` => `{word_en}`
- POST `/api/translate` => `{word_en}`
- POST `/api/rev_translate` => `{word_ru}`
- POST `/api/remember` => `{word_en}`

### Admin
- GET `/api/admin/word?id=int` => 
```
{
'word_en': word.word_en,
'word_ru': word.word_ru,
'word_az': word.word_az
}
```
- POST `/api/admin/word` => 
```
{
'word_en': word_en,
'word_ru': word_ru,
'word_az': word_az
}
```
- PUT `/api/admin/word`
  - Request
  ```
  id: int
  ```
  - Response
  ```
  {
  'word_en': word_en,
  'word_ru': word_ru,
  'word_az': word_az
  }
  ```
- DELETE `/api/admin/word` 
  - Request
  ```
    id: int
  ```
  - Response 
  ```
  {'message': 'word was deleted'}
  ```
  

---
## DATABASE

* USERS

* WORDS

* LEARNED WORDS

* WORDS TO LEARN

* USER WORD TEST RESULT

---

## Running the Project

To run the entire application using Docker Compose, the project should be organized as follows:
```
.
├── frontend
└── backend
```

The `docker-compose.yml` file expects both frontend and backend directories to be located at the same level.

### Start

```bash
docker compose up --build
```
---

## Author

**Nurlan Aliev**  
Python Backend Developer  
[GitHub](https://github.com/Nurlan-Aliev)  
[LinkedIn](https://linkedin.com/in/nurlan-aliev/)
