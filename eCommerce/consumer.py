import json
import pika
from sys import path
from os import environ
import django



path.append(r'\eCommerce\eCommerce\settings.py') # Your path to settings.py
environ.setdefault('DJANGO_SETTINGS_MODULE', 'eCommerce.settings')
django.setup()

from item.models import Item

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='products', durable=True)

def callback(ch, method, properties, body):
    print(body)
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_liked':
        product = Item.objects.get(id=data)
        product.likes += 1
        product.save()
        print("Quote likes increased.")
channel.basic_consume(queue='products', on_message_callback=callback)
print("Started Consuming...")
channel.start_consuming()
channel.close()