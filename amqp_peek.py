#!/usr/bin/env python

import sys
from sys import argv
from amqplib import client_0_8 as amqp
from pprint import pprint

conn = amqp.Connection()
channel = conn.channel()

channel.queue_declare(argv[1], durable=True, auto_delete=False)

channel.basic_consume(
  queue=argv[1], 
  no_ack=False,
  callback=lambda message: sys.stdout.write(message.body))

channel.wait()
