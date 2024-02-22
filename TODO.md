# Books API ToDos

## `/books/`

- [X] `GET /api/books/{id}` — получение информации о книге.
- [X] `POST /api/books/` — создание книги с ID существующего автора.
- [ ] `POST /api/books/` + автор — создание книги с именем и фамилией автора создаёт книгу и автора.
- [ ] `PUT /api/books/{id}` — изменение или создание книги.
- [ ] `PATCH /api/books/{id}` — частичное изменение книги.
- [X] `DELETE /api/books/{id}` — удаление книги.
- [ ] Есть валидация ID автора.

## `/authors/`

- [X] `GET /api/authors/` — просмотр всех авторов.
- [X] `GET /api/authors/{id}` — просмотр всех книг автора.
- [X] `POST /api/authors/` — создание автора.
- [X] `DELETE /api/authors/{id}` — удаление автора вместе со всеми его книгами.
- [ ] Возможность создать автора при добавлении книги.
- [X] При удалении автора удаляются все его книги.

## Общее

- [ ] Написать тесты для каждого эндпоинта.
- [ ] Используются корректные коды состояния HTTP. Например, 404, если ресурс не найден, или 201, если ресурс создан.
- [ ] Разработать подробную документацию API.
  - Задокументировать, какие данные выдаёт/принимает каждый endpoint.

## Примеры запросов к API

```bash
curl --request GET \
    --url http://127.0.0.1:5000/api/books/ | jq

curl --request POST \
    --url http://127.0.0.1:5000/api/authors/ \
    --header 'Content-Type: application/json' \
    --data '{"first_name": "Александр", "middle_name": "Сергеевич", "last_name": "Пушкин"}' | jq

curl --request DELETE \
    --url http://127.0.0.1:5000/api/authors/4 

curl --request POST \
    --url http://127.0.0.1:5000/api/books/ \
    --header 'Content-Type: application/json' \
    --data '{"title": "The New Book", "author": {"id": 1}}' | jq
```