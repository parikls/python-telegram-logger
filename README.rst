=====
Python Telegram Logger
=====

Provide simple logger which posts messages to a telegram in markdown format. Use a separate thread for a dispatching. Support many chats

Quick start
-----------

1. Add logger to your dict config:

.. code-block:: python

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "telegram": {
                "class": "python_telegram_logger.TelegramHandler",
                "token": "token",
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
    logger.info("TEST")


