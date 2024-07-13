import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    # Create formatters
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    simple_formatter = logging.Formatter("%(levelname)s - %(message)s")

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.NOTSET)
    console_handler.setFormatter(simple_formatter)

    # Create file handler and set level to debug
    file_handler = RotatingFileHandler("app.log", maxBytes=1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Create and configure root logger
    logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])

    # # Create a custom logger
    # logger = logging.getLogger("config")
    # logger.setLevel(logging.DEBUG)
    # logger.addHandler(console_handler)
    # logger.addHandler(file_handler)


# Run setup_logging function to configure logging
setup_logging()
