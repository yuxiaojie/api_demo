import multiprocessing
import os

from app.config import LOG_PATH

user = 'www'
group = 'www'

debug = False
deamon = False
loglevel = 'info'
bind = '0.0.0.0:12345'
max_requests = 50000
worker_connections = 50000

x_forwarded_for_header = "X-Real-IP"

# 启动的进程数
workers = multiprocessing.cpu_count()
# workers = 3
worker_class = "gevent"

accesslog = os.path.join(LOG_PATH, 'access.log')
access_log_format = '%({X-Real-IP}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = os.path.join(LOG_PATH, 'error.log')

timeout = 60
