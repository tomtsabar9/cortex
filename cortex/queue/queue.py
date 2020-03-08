import pika
from urllib.parse import urlparse

class MsgQueue:
    def __init__(self, url):
        purl = urlparse(url)
        self.type = purl.scheme

        if self.type == "rabbitmq":
            credentials = pika.PlainCredentials('guest', 'guest')
            connection = pika.BlockingConnection(pika.ConnectionParameters(purl.hostname, purl.port, purl.path, credentials))
            self.msgChannel = connection.channel() 
        else:
            raise NotImplementedError

    def add_consumer(self, q_name, callback):
        if self.type == "rabbitmq":
            self.msgChannel.queue_declare(queue=q_name)
            self.msgChannel.basic_consume(queue=q_name, on_message_callback=callback)
        else:
            raise NotImplementedError

    def add_exchange(self, ex_name, ex_type):
        if self.type == "rabbitmq":
            self.msgChannel.exchange_declare(exchange=ex_name, exchange_type=ex_type)
        else:
            raise NotImplementedError

    def bind_exchange(self, ex_name, q_name):
        if self.type == "rabbitmq":
            self.msgChannel.queue_declare(queue=q_name)
            self.msgChannel.queue_bind(exchange=ex_name,queue=q_name)
        else:
            raise NotImplementedError

    def publish(self, ex_name, q_name, msg):
        if self.type == "rabbitmq":
            self.msgChannel.basic_publish(exchange=ex_name, routing_key=q_name, body=msg)
        else:
            raise NotImplementedError
        
    def consume(self):
        if self.type == "rabbitmq":
            self.msgChannel.start_consuming()
        else:
            raise NotImplementedError