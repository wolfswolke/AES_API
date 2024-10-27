import logging
import traceback
import sys

LOG_COLORS = {
    logging.DEBUG: "\033[94m",  # Blue
    logging.INFO: "\033[92m",  # Green
    logging.WARNING: "\033[93m",  # Yellow
    logging.ERROR: "\033[91m",  # Red
    logging.CRITICAL: "\033[95m"  # Magenta
}
RESET_COLOR = "\033[0m"


class ColoredConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            color = LOG_COLORS.get(record.levelno, RESET_COLOR)
            log_message = self.format(record)
            colored_message = f"{color}{log_message}{RESET_COLOR}"
            self.stream.write(colored_message + self.terminator)
            self.flush()
        except Exception:
            self.handleError(record)


def setup_logger(name, level=logging.DEBUG):
    """
    Sets up a logger with the specified name and level.

    Args:
    - name (str): The name of the logger.
    - level (int): The logging level (default: logging.DEBUG).

    Returns:
    - logger (logging.Logger): Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = ColoredConsoleHandler()
    handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


def log_exception(logger, exc):
    """
    Logs an exception with detailed information.

    Args:
    - logger (logging.Logger): The logger instance.
    - exc (Exception): The exception to log.
    """
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb_info = traceback.extract_tb(exc_tb)
    filename, line, func, text = tb_info[-1]

    logger.error(f"Exception in {func} at {filename}:{line} - {exc_value} (Code: {text})")


# Example usage of the logger setup function
def some_function():
    logger = setup_logger('SomeFunctionLogger', logging.ERROR)
    try:
        # Simulate an error
        some_list = [1, 2, 3]
        print(some_list[5])
    except Exception as e:
        log_exception(logger, e)


if __name__ == "__main__":
    logger = setup_logger('MainLogger', logging.DEBUG)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    some_function()
