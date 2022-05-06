# Instructions

## Docker Compose

```
$ docker-compose build auth
$ docker-compose build taskmanager
$ docker-compose up -d
$ docker-compose exec auth python src/manage.py migrate
$ docker-compose exec auth python src/manage.py createsuperuser
$ docker-compose exec auth python src/manage.py collectstatic
$ docker-compose exec taskmanager python src/manage.py migrate
$ docker-compose exec taskmanager python src/manage.py createsuperuser
$ docker-compose exec taskmanager python src/manage.py collectstatic
```