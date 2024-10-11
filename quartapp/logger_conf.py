import logging

# Set up logging
errorlog = "/var/log/gunicorn/error.log"
logger = logging.getLogger('gunicorn.error')
logger.setLevel(logging.DEBUG)

# Create a file handler to log messages to a file
file_handler = logging.FileHandler(errorlog)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create a console handler to log messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)