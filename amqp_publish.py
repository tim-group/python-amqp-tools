#!/usr/bin/env python

import sys
from sys import argv
from amqplib import client_0_8 as amqp

host = 'localhost'
queue = argv[1]
message = " ".join(argv[2:])

if ':' in queue:
  host, queue = queue.split(':')


conn = amqp.Connection(host)
channel = conn.channel()
channel.queue_declare(queue, durable=True, auto_delete=False)

while True:
  channel.basic_publish(amqp.Message(message), exchange='', routing_key=queue)
