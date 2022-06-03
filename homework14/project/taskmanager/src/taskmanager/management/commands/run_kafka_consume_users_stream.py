from django.core.management.base import BaseCommand
from django.conf import settings

import pickle
from kafka import KafkaConsumer

from taskmanager.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(User.objects.all())
        broker = settings.BROKER_SERVER
        consumer = KafkaConsumer(
            'users-stream',
            bootstrap_servers=[broker, ]
        )

        for message in consumer:
            deserialized_data = pickle.loads(message.value)
            cud_funcs = {
                'user_created': self.create_user,
                'user_updated': self.update_user,
                'user_deleted': self.delete_user
            }
            event_name = deserialized_data['event_name']
            user_func = cud_funcs.get(event_name, None)
            if user_func:
                user_func(deserialized_data['data'])
                print(User.objects.all())

    # Custom Methods

    def create_user(self, user_data):
        user = User(
            system_id=user_data['system_id'],
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data['role'],
        )
        user.save()

    def update_user(self, user_data):
        try:
            user = User.objects.get(system_id=user_data['system_id'])
            user.username = user_data['username']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.role = user_data['role']
            user.save()
        except Exception as e:
            print(e)

    def delete_user(self, user_data):
        User.objects.filter(system_id=user_data['system_id']).delete()
