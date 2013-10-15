#!/usr/bin/env python

import sys
from sys import argv
from amqplib import client_0_8 as amqp
from pprint import pprint

conn = amqp.Connection()
channel = conn.channel()

channel.queue_declare(argv[1], durable=True, auto_delete=False)

def consume_message(message):
    sys.stdout.write(message.body)
    channel.basic_ack(message.delivery_tag)

channel.basic_consume(
  queue=argv[1], 
  no_ack=False,
  callback=consume_message)

channel.wait()
