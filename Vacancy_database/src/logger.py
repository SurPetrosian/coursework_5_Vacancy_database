import logging


def logger_setup() -> logging.Logger:
    """Logger setter"""
    my_logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(file_formatter)
    my_logger.addHandler(console_handler)
    my_logger.setLevel(logging.DEBUG)
    return my_logger


general_logger = logger_setup()
