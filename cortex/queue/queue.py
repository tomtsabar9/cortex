import pika
import os
from urllib.parse import urlparse

class MsgQueue:
    """
    Wraps general queue:
    Currently implenting support only in rabbitmq.
    """
    def url_init(self, url):
        """
        Init queue from url.
        Supports multiple queues.
        Take credentials from env var.
        """
        purl = urlparse(url)
        self.type = purl.scheme

        username = os.environ.get('_USERNAME')
        password = os.environ.get('_PASSWORD')

        if self.type == "rabbitmq":

            credentials = pika.PlainCredentials(username, password)
            connection = pika.BlockingConnection(pika.ConnectionParameters(purl.hostname, purl.port, purl.path, credentials))
            self.msgChannel = connection.channel() 
        elif self.type == "dummy":
            pass
        else:
            raise NotImplementedError

    def channel_init(self, channel):
        """
        There no use for that yet.
        """
        raise NotImplementedError

    def __init__(self, url = None, channel = None):
        """
         
        """
        if channel == None:
            self.url_init(url)
        else:
            self.channel_init(channel)

    def add_consumer(self, q_name, callback):
        """
        Adds a consumer to the queue
        """
        if self.type == "rabbitmq":
            self.msgChannel.queue_declare(queue=q_name)
            self.msgChannel.basic_consume(queue=q_name, on_message_callback=callback)
        elif self.type == "dummy":
            pass
        else:
            raise NotImplementedError


    def add_queue(self, q_name):
        """
        Adds a queue to the channel
        """
        if self.type == "rabbitmq":
            self.msgChannel.queue_declare(q_name)
        elif self.type == "dummy":
            pass
        else:
            raise NotImplementedError

    def add_exchange(self, ex_name, ex_type):
        """
        Adds an exchange to the channel
        """
        if self.type == "rabbitmq":
            self.msgChannel.exchange_declare(exchange=ex_name, exchange_type=ex_type)
        elif self.type == "dummy":
            pass
        else:
            raise NotImplementedError

    def bind_exchange(self, ex_name, q_name):
        """
        Binds queue to an exchange
        """
        if self.type == "rabbitmq":
            self.msgChannel.queue_declare(queue=q_name)
            self.msgChannel.queue_bind(exchange=ex_name,queue=q_name)
        elif self.type == "dummy":
            pass
        else:
            raise NotImplementedError

    def publish(self, ex_name, q_name, msg):
        """
        Publish data to exchange/queue
        """
        if self.type == "rabbitmq":
            self.msgChannel.basic_publish(exchange=ex_name, routing_key=q_name, body=msg)
        elif self.type == "dummy":
            pass
        else:
            raise NotImplementedError
        
    def consume(self):
        """
        Consumes queue
        """
        if self.type == "rabbitmq":
            self.msgChannel.start_consuming()
        elif self.type == "dummy":
            pass
        else:
            raise NotImplementedError