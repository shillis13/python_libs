import logging
from contextlib import contextmanager
from functools import wraps


def setup_logging(level=logging.INFO):
    """
    Set up the basic configuration for the logging system.
    Args:
        level (int): The logging level, e.g., logging.INFO, logging.DEBUG.
    Example:
        setup_logging(logging.DEBUG)
    """
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=level)


@contextmanager
def log_block(name):
    """
    Context manager for logging the entry and exit of a code block.
    Args:
        name (str): The name of the block for logging purposes.
    Example:
        with log_block("process_data"):
            # code block
    """
    logging.info(f"Entering block: {name}")
    try:
        yield
    finally:
        logging.info(f"Exiting block: {name}")


def log_function(func):
    """
    Decorator for logging function calls with their arguments and return values.
    Args:
        func (function): The function to be wrapped for logging.
    Returns:
        function: The wrapped function.
    Example:
        @log_function
        def add(a, b):
            return a + b
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logging.info(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        logging.info(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper


# Decorator to handle non-string inputs in logging functions
def handle_non_string_inputs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Convert all args to strings
        str_args = [str(arg) for arg in args]
        # Convert all key-value pairs in kwargs to strings
        str_kwargs = {k: str(v) for k, v in kwargs.items()}
        return func(*str_args, **str_kwargs)
    return wrapper


@handle_non_string_inputs
def log_info(message):
    """
    Log an informational message.
    Args:
        message (str): The message to log.
    Example:
        log_info("Data processing complete.")
    """
    logging.info(message)


@handle_non_string_inputs
def log_error(message):
    """
    Log an error message.

    Args:
        message (str): The message to log.

    Example:
        log_error("Data processing failed.")
    """
    logging.error(message)


@handle_non_string_inputs
def log_debug(message):
    """
    Log an informational message.

    Args:
        message (str): The message to log.

    Example:
        log_info("Data processing complete.")
    """
    logging.debug(message)


@handle_non_string_inputs
def log_out(message):
    """
    Output a message without any additional formatting.

    Args:
        message (str): The message to output.
    """
    print(message)


