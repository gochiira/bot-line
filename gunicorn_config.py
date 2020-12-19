import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
bind = '0.0.0.0:1204'
umask = 0o007
reload = True
timeout = 1000

# logging
accesslog = '-'
errorlog = '-'
