from app import config
from celery import Celery


app = Celery('tasks', broker=config.CELERY_BROKER_URL)
app.conf.update({k: getattr(config, k) for k in dir(config)
                 if type(getattr(config, k)) is str and not k.startswith('_')})
