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

$ docker-compose exec taskmanager python src/manage.py run_kafka_consume_users_stream
```

## Notes

```
curl -X POST -d "grant_type=password&username=admin&password=admin12345" -u"m3vbKHa5dtiFmw4eb1VV4jMcIJELXYW11CV7WtL8:uODkkvsI4j9mUqtCECdVc3GCKWEgLCKPCIqsJCRk2li4oIDFi9mXXoGZFY7EPa7340Ex4BygS4XVrUigEm3wDg5ZSGLyIhTtpXaXKIusi3MIDnhYi6ynTM7Un2qVxQQO" http://localhost:3000/o/token/

curl -H "Authorization: Bearer uloyLp2mCC4kPswoSmv16Jw2Y1Bziy" http://localhost:3000/users/1/

curl -X POST -d "grant_type=password&username=test&password=test12345" -u"m3vbKHa5dtiFmw4eb1VV4jMcIJELXYW11CV7WtL8:uODkkvsI4j9mUqtCECdVc3GCKWEgLCKPCIqsJCRk2li4oIDFi9mXXoGZFY7EPa7340Ex4BygS4XVrUigEm3wDg5ZSGLyIhTtpXaXKIusi3MIDnhYi6ynTM7Un2qVxQQO" http://localhost:3000/o/token

docker exec broker \
kafka-topics --bootstrap-server broker:9092 \
             --create \
             --topic tasks

docker exec --interactive --tty broker \
kafka-console-consumer --bootstrap-server broker:9092 \
                       --topic tasks \
                       --from-beginning

docker exec --interactive --tty broker \
kafka-console-producer --bootstrap-server broker:9092 \
                       --topic tasks
```