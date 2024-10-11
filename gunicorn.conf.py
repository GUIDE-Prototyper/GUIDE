import multiprocessing

max_requests = 1000
max_requests_jitter = 50
loglevel = 'debug'
accesslog = "/var/log/gunicorn/access.log"
bind = "0.0.0.0:8000"

num_cpus = multiprocessing.cpu_count()
workers = (num_cpus * 2) + 1
threads = 2
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120