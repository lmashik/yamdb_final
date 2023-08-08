# Проект yamdb_final

Статус workflow: ![badge](https://github.com/lmashik/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

----------------------------------------
## Описание

Проект YaMDb собирает отзывы (Review) пользователей на произведения 
(Title).  
Произведения делятся на категории. Список категорий (Category) может 
быть расширен.  
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм 
или послушать музыку.  
К каждому произведению можно оставить отзыв и оценку, на основе оценок 
рассчитывается рейтинг.  
Каждый отзыв может быть прокомментирован.

----------------------------------------
## Используемые технологии

 - Python 3.7
 - Django Rest Framework 3.12.4 (библиотека для преобразования Django-приложения в REST API)
 - Postman (графическая программа для тестирования API)
 - Postgres (система управления базами данных)
 - Docker (программная платформа контейнеризации)
 - Docker Compose (средство для определения и запуска приложений Docker с несколькими контейнерами)
 - Nginx (веб-сервер для статики)
 - Gunicorn (веб WSGI-сервер)
 - GitHub Actions (сервис автоматизации тестирования, размещения и запуска проекта на сервере)

----------------------------------------
## Установка

1. Клонируем репозиторий и перейти в директорию infra в командной строке
```bash
git clone https://github.com/lmashik/infra_sp2.git
```

```bash
cd infra_sp2/infra
```

2. Создаем файл .env для переменных виртуального окружения и заходим в него
```bash
nano .env
```

3. Заполняем файл значениями переменных из файла .env.example
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<secret_key>
```

4. Создаем образ и контейнеры, запускаем контейнеры в фоновом режиме
```bash
sudo docker-compose up -d
```

5. Выполняем миграции внутри контейнера web
```bash
sudo docker-compose exec web python manage.py migrate
```

6. Открываем проект по адресу http://localhost/api/v1  
или его административную часть по адресу http://localhost/admin/

При необходимости наполняем базу резервными данными
7. Узнаем id контейнера (web), в который нужно скопировать дамп
```bash
sudo docker ps
```

8. Копируем дамп в контейнер web
```bash
sudo docker cp fixtures.json <CONTAINER_ID>:app/
```

9. Заливаем данные в базу
```bash
sudo docker-compose exec web python manage.py loaddata fixtures.json
```

10. Удаляем дамп из контейнера
```bash
sudo docker-compose exec web rm ./fixtures.json
```

----------------------------------------
## Примеры запросов к API

### Регистрация
Для получения кода подтверждения необходимо отправить POST запрос 
к эндпоинту http://158.160.17.165/api/v1/auth/signup/, в теле запроса 
указать:

```
{
"email": "user@example.com",
"username": "user"
}
```

При успешном завершении запроса вы получите письмо с кодом подтверждения 
(confirmation_code) на адрес email

Для получения токена необходимо отправить POST запрос к эндпоинту 
http://158.160.17.165/api/v1/auth/token/, в теле запроса указать:

```
{
"username": "user",
"confirmation_code": "string"
}
```

При успешном завершении запроса вы получите в ответ токен:

```
{
"token": "string"
}
```

### Формат запросов
Запрос осуществляется посредством протокола HTTP 1.1 на адрес, 
соответствующий ресурсу. HTTP-запросы должны содержать заголовок:
_Authorization: Bearer <access_token>_

### Формат ответа
Ответ сервиса представляет собой JSON-документ в кодировке UTF-8, 
содержимое зависит от запроса.

### Ресурсы

Ресурс - часть системы, с которой можно работать. В YaMDb ресурсами 
являются: категории, жанры, произведения, отзывы, комментарии, пользователи.
У каждого ресурса уникальный URL. Для получения списка доступных ресурсов 
выполните GET-запрос к корневому URL API http://158.160.17.165/api/v1/, 
а также к URL: 
http://158.160.17.165/api/v1/titles/{title_id}/reviews/ 
и http://158.160.17.165/api/v1/titles/{title_id}/reviews/{review_id}/comments/

Возможные ресурсы API:

```
/api/v1/categories/ (GET, POST)

/api/v1/categories/{slug}/ (DELETE)

/api/v1/genres/ (GET, POST)

/api/v1/genres/{slug}/ (DELETE)

/api/v1/titles/ (GET, POST)

/api/v1/titles/{titles_id}/ (GET, PATCH, DELETE)

/api/v1/titles/{title_id}/reviews/ (GET, POST)

/api/v1/titles/{title_id}/reviews/{review_id}/ (GET, PATCH, DELETE)

/api/v1/titles/{title_id}/reviews/{review_id}/comments/ (GET, POST)

/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ (GET, PATCH, DELETE)

/api/v1/users/ (GET, POST)

/api/v1/{username}/ (GET, PATCH, DELETE)

/api/v1/users/me/ (GET, PATCH)
```

----------------------------------------
## Авторы проекта
Автор yamdb_final: Мария Лапикова (Михайлова), mashik.mikhaylova@yandex.ru  
Авторы YaMDb: Шовтюк Елена, Лапикова (Михайлова) Мария, Пиголкин Андрей
