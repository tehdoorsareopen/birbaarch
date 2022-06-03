import pickle

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kafka import KafkaProducer

from .models import User


def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    print(excp)


# CUD Events

@receiver(post_save, sender=User)
def produce_user_created_event(sender, instance, created, **kwargs):
    if created:
        broker = settings.BROKER_SERVER
        producer = KafkaProducer(bootstrap_servers=broker)
        user = instance
        data = {
            'event_name': 'user_created',
            'data': {
                'system_id': user.system_id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role.name,
            }
        }

        serialized_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        producer.send(
            'users-stream', serialized_data
        ).add_callback(on_send_success).add_errback(on_send_error)


@receiver(post_save, sender=User)
def produce_user_updated_event(sender, instance, created, **kwargs):
    if not created:
        broker = settings.BROKER_SERVER
        producer = KafkaProducer(bootstrap_servers=broker)
        user = instance
        data = {
            'event_name': 'user_updated',
            'data': {
                'system_id': user.system_id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role.name,
            }
        }

        serialized_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        producer.send(
            'users-stream', serialized_data
        ).add_callback(on_send_success).add_errback(on_send_error)


@receiver(post_delete, sender=User)
def produce_user_deleted_event(sender, instance, **kwargs):
    broker = settings.BROKER_SERVER
    producer = KafkaProducer(bootstrap_servers=broker)
    user = instance
    data = {
        'event_name': 'user_deleted',
        'data': {
            'system_id': user.system_id,
        }
    }

    serialized_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
    producer.send(
        'users-stream', serialized_data
    ).add_callback(on_send_success).add_errback(on_send_error)
