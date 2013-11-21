#!/usr/bin/env python

import sys
from sys import argv
from amqplib import client_0_8 as amqp
from time import time, sleep


RATE = 200 # messages per second max

sent_times = [0] * RATE

conn = amqp.Connection()
channel = conn.channel()
channel.basic_qos(0, RATE, False)

channel.queue_declare(argv[1], durable=True, auto_delete=False)
channel.queue_declare(argv[2], durable=True, auto_delete=False)

def copy(message):
  now = time()
  
  global sent_times
  
  sent_times.insert(0, now)
  sent_times.pop()
  
  delta = now - sent_times[-1]
  
  if delta < 1.0:
    sleep(1.0 - delta)
  
  channel.basic_publish(message, exchange='', routing_key=argv[2])
  channel.basic_ack(message.delivery_tag)

channel.basic_consume(
  queue=argv[1], 
  no_ack=False,
  callback=copy)

while True:
  channel.wait()