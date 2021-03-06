#!/usr/bin/env python
import pika
import os
from fastfibonacci.fastfibonacci import fibonacci

credentials = pika.PlainCredentials(
    username=os.environ['RABBITMQ_DEFAULT_USER'],
    password=os.environ['RABBITMQ_DEFAULT_PASS']
)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq',
        credentials=credentials
    )
)

channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fibonacci(n)

    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=str(response)
    )
    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
