#!/usr/bin/env python

import sys
from sys import argv
from amqplib import client_0_8 as amqp

from_host = 'localhost'
from_queue = argv[1]
to_host = 'localhost'
to_queue = argv[2]

if ':' in from_queue:
  from_host, from_queue = from_queue.split(':')

if ':' in to_queue:
  to_host, to_queue = to_queue.split(':')


from_conn = amqp.Connection(from_host)
from_channel = from_conn.channel()
from_channel.queue_declare(from_queue, durable=True, auto_delete=False)

to_conn = amqp.Connection(to_host)
to_channel = to_conn.channel()
to_channel.queue_declare(to_queue, durable=True, auto_delete=False)

from_channel.basic_consume(
  queue=from_queue,
  no_ack=True,
  callback=lambda message: to_channel.basic_publish(message, exchange='', routing_key=to_queue))

while True:
  from_channel.wait()