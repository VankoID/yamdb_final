### Краткое описание проекта YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».


### Шаблон наполнения env-файла
```
SECRET_KEY = key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
### Стек технологий
gunicorn, Nginx, Docker, docker-compose, PostgreSQL


### Запуск контейнера и приложения

Перейти в репозиторий для запуска докера

```
cd infra/
```

Запуск docker-compose

```
docker-compose up -d --build

```
Проведите миграции
```
docker-compose exec web python manage.py migrate
```

Cоздайте суперпользователя
```
docker-compose exec web python manage.py createsuperuser
```

Остановку контейнеров проведите командой
```
docker-compose down -v 
```

### Автор проекта

Ivan Dudarev

https://github.com/VankoID/yamdb_final/actions/workflows/yamdb_workflow/badge.svg
