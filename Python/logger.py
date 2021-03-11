import logging

logger = logging.getLogger('__main__')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%Y %H:%M:%S %p')

consoleHeader = logging.StreamHandler()
consoleHeader.setFormatter(formatter)
consoleHeader.setLevel(logging.INFO)

logger.addHandler(consoleHeader)
