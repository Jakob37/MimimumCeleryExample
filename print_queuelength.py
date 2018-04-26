#!/usr/bin/env python3

import app
from app import celery

print('Inspecting the queue...')
inspect = celery.control.inspect()
scheduled = inspect.scheduled()
reserved = inspect.reserved()
active = inspect.active()

worker_keys = list(reserved.keys())
print('Found workers: {}'.format(worker_keys))
primary_worker = worker_keys[0]
print('Using worker: {}'.format(primary_worker))
queue_size = len(reserved[primary_worker])

print('Scheduled size: {}'.format(len(scheduled[primary_worker])))
print('Reserved size: {}'.format(queue_size))

print('Current job: {}'.format(active[primary_worker]))

