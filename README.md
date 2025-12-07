## routers
### AUTH
  * `GET` - `/auth/about_me` - get info about user
  * `POST` - `/auth/sign_up` - create new account
  * `POST` - `/auth/refresh` - get new access token by refresh
  * `POST` - `/auth/login` - make login
  * `POST` - `/auth/logout` - make logout

---

### api 
  * `GET` - `/api/` - get 10 words
  * `GET` - `/api/learned_word_count` - count of learned words

  * `POST` - `/api/learned` - word was learned
  * `POST` - `/api/to_learn` -  add word to the list need learn
---
  * `GET` - `/api/constructor` - get 10 words for constructor
  * `GET` - `/api/translate` - get 10 words in english and 4 answer options
  * `GET` - `/api/rev_translate` - get 10 words in russian and 4 answer options
  * `POST` - `/api/test` - check correct answers
---
  * `POST` - `/api/admin/word` - add new word
  * `DELETE` - `/api/admin/word` - delete word
  * `PATCH` - `/api/admin/word` - update word
---
