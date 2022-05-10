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
            user_func = self.delete_user if deserialized_data['action'] == 'delete' else self.update_or_create_user
            user_func(deserialized_data['user'])
            print(User.objects.all())

    # Custom Methods

    def update_or_create_user(self, user_data):
        obj, created = User.objects.update_or_create(
            system_id=user_data['system_id'],
            defaults={
                'username': user_data['username'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
            },
        )

    def delete_user(self, user_data):
        User.objects.filter(system_id=user_data['system_id']).delete()
