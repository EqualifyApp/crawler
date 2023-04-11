import logging

# Add logging to each file with
#   from utils.watch import logger


"""
    ## Watch
    _utils.watch.py_
    ~~~~~~~~~~~~~~~~~

    Summary Statement Goes Here
    Short tl;dr of this module that is no longer than 2 sentences

    Overview:
    ~~~~~~~~~


    Usage:
    ------

    The `logging.getLogger()` function returns a logger instance with the specified name. If a logger already exists with the same name, it will be returned. Otherwise, a new logger will be created.

    This module exports a single logger instance named "A11yLogger". This logger outputs log records to the console, with a log level of INFO or higher.

    Example:

    .. code-block:: python

       import logging
       from logging_config import logger

       logger.debug("Debug message")
       logger.info("Info message")
       logger.warning("Warning message")
       logger.error("Error message")
       logger.critical("Critical message")


    Functions and classes:
    ----------------------

    The `logging_config` module exports the following functions and classes:

    .. currentmodule:: logging_config

    .. autosummary::
       :nosignatures:

       logger

    Variables:
    ----------

    The `logging_config` module exports the following variables:

    - `A11y🪵 `: The default logger instance for the A11y🪵.


"""
# Set up logger: "A11yLogger"
logger = logging.getLogger("A11y🪵 ")

# Check if logger already has handlers
if not logger.hasHandlers():
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to info
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)

def configure_logger():
     # Use the logger from logging_config.py
     global logger
     logger = logging.getLogger("A11y🪵 ")