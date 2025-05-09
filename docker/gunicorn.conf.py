# flake8: noqa

import multiprocessing

wsgi_app = 'entrypoint:application'
bind = ['0.0.0.0:8000']
preload_app = True
daemon = False

accesslog = '-'
errorlog = '-'
loglevel = 'debug'

# Don't increase workers or it'll break plotly express:

workers = 1

# But in an ideal world:
#
# workers = multiprocessing.cpu_count() * 2 + 1
# threads = 
# worker_class = 'gevent'  # TODO: test this out

# TODO: syslog setttings?
