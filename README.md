# yamdb_final
yamdb_final

![badge](https://github.com/lmashik/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)



# Проект infra_sp2

## Описание
Проект infra_sp2 позволяет развернуть проект YaMDb на ВМ с помощью трех 
контейнеров: web, db, nginx.

Проект YaMDb собирает отзывы (Review) пользователей на произведения 
(Title).
Произведения делятся на категории. Список категорий (Category) может 
быть расширен.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм 
или послушать музыку.

## Используемые технологии

 - Python 3.7
 - Django Rest Framework 3.12.4 (библиотека для преобразования Django-приложения в REST API)
 - Postman (графическая программа для тестирования API)
 - Postgres (система управления базами данных)
 - Docker (программная платформа контейнеризации)
 - Docker Compose (средство для определения и запуска приложений Docker с несколькими контейнерами)
 - Nginx (веб-сервер для статики)
 - Gunicorn (веб WSGI-сервер)

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


## Авторы проекта
Автор infra_sp2: Мария Лапикова (Михайлова)  
Авторы YaMDb: Шовтюк Елена, Лапикова (Михайлова) Мария, Пиголкин Андрей
