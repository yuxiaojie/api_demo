from celery.schedules import crontab

from .delay_runnable import delay_do
from celery_worker import app

bg_gen_sn_qr = app.task(delay_do)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(30.0, alarm_print.s('hello world'), name='add every 10')
    print('setup periodic tasks success')
    # sender.add_periodic_task(crontab(hour=0, minute=16, day_of_month='1-31'), settle_accounts.s())\
