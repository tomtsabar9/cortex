import pika

from .parsers import *


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

def users_cons():

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
    msgChannel = connection.channel() 
    msgChannel.queue_declare(queue='users')
    msgChannel.basic_consume(queue='users', auto_ack=True, on_message_callback=callback)
    msgChannel.start_consuming()



if __name__ == '__main__':
    users_cons()