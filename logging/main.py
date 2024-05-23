import atexit
import json
import logging.config
import logging.handlers
import pathlib

logger = logging.getLogger("my_app")


def setup_logging():
    config_file = pathlib.Path("logging/config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)
        print("Loaded logging configuration:", config)
    logging.config.dictConfig(config=config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)


def main():
    setup_logging()
    logger.debug("debug message")
    logger.info("debug message")
    logger.warning("debug message")
    logger.error("debug message")
    logger.critical("debug message")
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()
