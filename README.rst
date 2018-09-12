=====
Python Telegram Logger
=====

Simple logger which dispatch messages to a telegram in markdown format.
Uses a separate thread for a dispatching.
Support many chats.
Support big messages (over 4096 chars)


Installation
-----------

.. code-block::
pip install python-telegram-logger


Quick start
-----------

1. Configure logger with dict config:

.. code-block:: python

    config = {
        ...
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "telegram": {
                "class": "python_telegram_logger.Handler",
                "token": "bot_token",
                "chat_ids": [123456789, -1234567891011],

            }
        },
        "tg": {
            "level": "INFO",
            "handlers": ["telegram",]
        }
    }


2. Use it!

.. code-block:: python

    import logging
    logger = logging.getLogger("tg")

    logger.info("test")

    try:
        raise Exception("raise!")
    except Exception:
        logger.exception("catch!")


