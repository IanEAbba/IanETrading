import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def setup_logging():
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")


    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)


    fh = TimedRotatingFileHandler("logs/runtime.log", when="midnight", interval=1, backupCount=7)
    fh.setFormatter(fmt)
    logger.addHandler(fh)