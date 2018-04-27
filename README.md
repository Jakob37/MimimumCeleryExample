# Installation

```
virtualenv venv
source venv/bin/activate

pip install flask
pip install redis
pip install celery

sudo apt install redis-tools
sudo apt install redis-server
```

# Usage

* Start the redis server: `redis-server`
* Start the Celery worker: `celery -A app.celery --concurrency=1 worker`
* Run commands:

```
import app
app.task.delay(arguments)
```

# Adding some long-running jobs

30 second jobs, printing every fifth second.

```
app.step_delay.delay(30, 5)
```

# Investigating the queue

Using the inspect control. Stack Overflow: https://stackoverflow.com/questions/5544629/retrieve-list-of-tasks-in-a-queue-in-celery

Note! This only gives information about tasks that are claimed by Celery, not everything in queue.

Also, speed up by `inspect('celery@mysite')` rather than the complete thing.

```
> from app import celery
> i = celery.control.inspect()
> i.active() # Shows the currently running
> i.reserved() # Shows the queue
```

Digging into the queue.

```
> r = i.reserved()
> list(r.keys())
# list of workers
> {'acknowledged': False,
 'args': '(30, 5)',
 'delivery_info': {'exchange': '',
 'priority': 0,
 'redelivered': None,
 'routing_key': 'celery'},
 'hostname': 'celery@computer',
 'id': '0f38bf8f-ed7e-40fa-a920-faaf0f2ec741',
 'kwargs': '{}',
 'name': 'app.step_delay',
 'time_start': None,
 'type': 'app.step_delay',
 'worker_pid': None}
```

# Example of getting REDIS-queue count

Command-line:

```
redis-cli -h localhost -p 6379 -n 0 llen celery
```

Programmatically:

```
import redis
red = redis.Redis(host='localhost', port=6379, db=0)
red.llen('celery')
```

