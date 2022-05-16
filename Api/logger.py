import logging

name_log = 'Globant'

logger = logging.getLogger(name_log)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '[%(asctime)s] - (%(levelname)s) %(lineno)4s: %(message)s', '%d %H:%M'
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler("{}.log".format(name_log))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)