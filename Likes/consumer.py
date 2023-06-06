import json
import pika
import django
from sys import path
from os import environ



path.append(r'\Likes\Likes\settings.py') #Your path to settings.py file
environ.setdefault('DJANGO_SETTINGS_MODULE', 'Likes.settings') 
django.setup()

from marks.models import Product

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='marks')

def callback(ch, method, properties, body):
    print("Received in likes...")
    print(body)
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product.objects.create(id=data['id'], name=data['name'])
        product.save()
        print("product created")
    elif properties.content_type == 'product_updated':
        product = Product.objects.get(id=data['id'])
        product.name = data['name']
        product.save()
        print("product updated")
    elif properties.content_type == 'product_deleted':
        product = Product.objects.get(id=data)
        product.delete()
        print("product deleted")

channel.basic_consume(queue='marks', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()
channel.close()