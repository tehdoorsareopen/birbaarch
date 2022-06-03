import pickle

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver, Signal

from kafka import KafkaProducer

from .models import Task


# Custom signals

new_task_added = Signal()
task_completed = Signal()
tasks_reassigned = Signal()


# Kafka functions

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)


def on_send_error(excp):
    print(excp)


# Business Events

@receiver(new_task_added, sender=Task)
def produce_new_task_added_event(sender, instance, **kwargs):
    print(instance, flush=True)
    broker = settings.BROKER_SERVER
    producer = KafkaProducer(bootstrap_servers=broker)
    task = instance
    data = {
        'event_name': 'new_task_added',
        'data': {
            'system_id': task.system_id,
        }
    }

    serialized_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
    producer.send(
        'tasks', serialized_data
    ).add_callback(on_send_success).add_errback(on_send_error)


@receiver(task_completed, sender=Task)
def produce_task_completed_event(sender, instance, **kwargs):
    print(instance, flush=True)
    broker = settings.BROKER_SERVER
    producer = KafkaProducer(bootstrap_servers=broker)
    task = instance
    data = {
        'event_name': 'task_completed',
        'data': {
            'system_id': task.system_id,
        }
    }

    serialized_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
    producer.send(
        'tasks', serialized_data
    ).add_callback(on_send_success).add_errback(on_send_error)


@receiver(tasks_reassigned, sender=Task)
def produce_tasks_reassigned_event(sender, instances, **kwargs):
    # bulk TODO
    pass


# CUD Events

@receiver(post_save, sender=Task)
def produce_task_created_event(sender, instance, created, **kwargs):
    if created:
        broker = settings.BROKER_SERVER
        producer = KafkaProducer(bootstrap_servers=broker)
        task = instance
        data = {
            'event_name': 'task_created',
            'data': {
                'system_id': task.system_id,
                'name': task.name,
                'description': task.description,
                'created_by': task.created_by.system_id,
                'assigned_on': task.assigned_on.system_id,
                'completed': task.completed,
                'created': task.created,
                'updated': task.updated,
            }
        }

        serialized_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        producer.send(
            'tasks-stream', serialized_data
        ).add_callback(on_send_success).add_errback(on_send_error)


@receiver(post_save, sender=Task)
def produce_task_updated_event(sender, instance, created, **kwargs):
    if not created:
        broker = settings.BROKER_SERVER
        producer = KafkaProducer(bootstrap_servers=broker)
        task = instance
        data = {
            'event_name': 'task_updated',
            'data': {
                'system_id': task.system_id,
                'name': task.name,
                'description': task.description,
                'created_by': task.created_by.system_id,
                'assigned_on': task.assigned_on.system_id,
                'completed': task.completed,
                'created': task.created,
                'updated': task.updated,
            }
        }

        serialized_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        producer.send(
            'tasks-stream', serialized_data
        ).add_callback(on_send_success).add_errback(on_send_error)


@receiver(post_delete, sender=Task)
def produce_task_deleted_event(sender, instance, **kwargs):
    broker = settings.BROKER_SERVER
    producer = KafkaProducer(bootstrap_servers=broker)
    task = instance
    data = {
        'event_name': 'task_deleted',
        'data': {
            'system_id': task.system_id,
        }
    }

    serialized_data = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
    producer.send(
        'tasks-stream', serialized_data
    ).add_callback(on_send_success).add_errback(on_send_error)
