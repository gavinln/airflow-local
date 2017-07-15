from celery import Celery

app = Celery('celery_tasks',
             broker='amqp://guest:guest@localhost:5672//')


@app.task
def add(x, y):
    return x + y
