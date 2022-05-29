#!/usr/bin/env python
import pika
import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='vidpit_auth',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


fibonacci_rpc = FibonacciRpcClient()

number = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NTI2MjQ0OTIsInN1YiI6IjM4MjdhYTVmLWFkNzctNDMwMy05ZTYzLWJiZmE4N2E1ZTNiNyJ9.z0Ev9hI4psj-I_f7sPJNUv9SROHaINH0w5kGlhRhMek"
print(f" [x] Requesting ({number})")
response = fibonacci_rpc.call(number)
print(" [.] Got %r" % response)