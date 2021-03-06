#!/usr/bin/env python
import pika
import uuid
import time
import os

class FibonacciRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials(
            username=os.environ['RABBITMQ_DEFAULT_USER'],
            password=os.environ['RABBITMQ_DEFAULT_PASS']
        )

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='rabbitmq',
                credentials=credentials
            )
        )

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue=self.callback_queue
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=str(n)
        )

        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

while True:
    print(" Waiting 5 seconds to start...")
    time.sleep(5)

    for n in range(1, 1001):
        print(" [x] Requesting fib(%r)" % n)
        response = fibonacci_rpc.call(n)
        print(" [.] Got %r" % response)
