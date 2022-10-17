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
Подгрузите статику
```
docker-compose exec web python manage.py collectstatic --no-input 
```

Остановку контейнеров проведите командой
```
docker-compose down -v 
```

### Автор проекта

Ivan Dudarev

### Ссылка на проект

http://51.250.18.154/admin/login/?next=/admin/

![Django-app workflow](https://github.com/VankoID/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

