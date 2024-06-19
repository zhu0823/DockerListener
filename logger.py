import logging
from logging.handlers import RotatingFileHandler


def setup_logger(name, log_file, max_bytes=10485760, backup_count=5):

    _logger = logging.getLogger(name)

    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    console_handler = logging.StreamHandler()

    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    _logger.addHandler(file_handler)
    _logger.addHandler(console_handler)

    return _logger


logger = setup_logger("Listener", "/logs/listener.log")
