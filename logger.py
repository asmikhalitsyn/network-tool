import logging

FORMAT_OF_LOGS = ('%(asctime)s - %(name)s - %(lineno)s - '
                  '%(levelname)s - %(funcName)s()- %(message)s')


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(FORMAT_OF_LOGS)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
