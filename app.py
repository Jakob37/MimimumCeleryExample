from celery import Celery
import time

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

from flask import Flask
flask_app = Flask(__name__)

flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(flask_app)

@flask_app.route('/')
def index():
    return '<html>index!</html>'

@celery.task()
def add_together(a, b):
    return a + b

@celery.task()
def step_delay(tot_time, print_intervals):
    
    for i in range(tot_time):
        if i % print_intervals == 0:
            print('Current time: {}'.format(i))
        time.sleep(1)
    print('Done!!')








