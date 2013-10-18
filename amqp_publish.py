#!/usr/bin/env python

import sys
from sys import argv
from amqplib import client_0_8 as amqp

host = 'localhost'
queue = argv[1]
count = int(argv[2])
message = sys.stdin.read()

if ':' in queue:
  host, queue = queue.split(':')

conn = amqp.Connection(host)
channel = conn.channel()
channel.queue_declare(queue, durable=True, auto_delete=False)

for i in xrange(count):
  channel.basic_publish(amqp.Message(message), exchange='', routing_key=queue)
