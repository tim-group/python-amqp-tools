#!/usr/bin/env python

# move messages from one queue to another, filtering out undesirable messages

import sys
from sys import argv
from amqplib import client_0_8 as amqp

from_host = 'localhost'
from_queue = argv[1]
to_host = 'localhost'
to_queue = argv[2]
shunt_host = 'localhost'
shunt_queue = argv[3]

filter_expression = argv[4]

if ':' in from_queue:
  from_host, from_queue = from_queue.split(':')

if ':' in to_queue:
  to_host, to_queue = to_queue.split(':')

if ':' in shunt_queue:
  shunt_host, shunt_queue = shunt_queue.split(':')

from_conn = amqp.Connection(from_host)
from_channel = from_conn.channel()
from_channel.queue_declare(from_queue, durable=True, auto_delete=False)

to_conn = amqp.Connection(to_host)
to_channel = to_conn.channel()
to_channel.queue_declare(to_queue, durable=True, auto_delete=False)

shunt_conn = amqp.Connection(shunt_host)
shunt_channel = shunt_conn.channel()
shunt_channel.queue_declare(shunt_queue, durable=True, auto_delete=False)

def process_message(message):
    if eval(filter_expression):
        shunt_channel.basic_publish(message, exchange='', routing_key=shunt_queue)
    else:
        to_channel.basic_publish(message, exchange='', routing_key=to_queue)

from_channel.basic_consume(
  queue=from_queue,
  no_ack=True,
  callback=process_message)

while True:
  from_channel.wait()
