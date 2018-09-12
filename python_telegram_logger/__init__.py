import logging.handlers
from queue import Queue

import requests

__version__ = 1.0
__author__ = "Dmytro Smyk"


class Formatter(logging.Formatter):
    """
    Default formatter for telegram
    """

    DEFAULT_FMT = """*%(levelname)s*\n_%(name)s:%(funcName)s_
    ``` %(message)s ``` %(exc)s
    """

    def __init__(self, fmt=None, *args, **kwargs):
        super().__init__(fmt or self.DEFAULT_FMT, *args, **kwargs)

    def format(self, record):
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        record = self.enrich_exception(record)
        message = self.formatMessage(record)

        return message

    def enrich_exception(self, record):
        """
        Enrich and do some formatting
        """
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        record.exc = None

        if record.exc_text:
            record.exc = record.exc_text

        if record.stack_info:
            record.exc = self.formatStack(record.stack_info)

        record.exc = "```%s```" % record.exc if record.exc else ""

        return record


class Handler(logging.handlers.QueueHandler):

    def __init__(self, token, chat_ids, disable_notifications=False, disable_preview=False):
        queue = Queue()
        super().__init__(queue)

        handler = LogMessageDispatcher(token, chat_ids, disable_notifications, disable_preview)
        handler.setFormatter(Formatter())
        listener = logging.handlers.QueueListener(queue, handler)
        listener.start()

    def prepare(self, record):
        return record


class LogMessageDispatcher(logging.Handler):
    TIMEOUT = 13  # seconds
    MAX_MSG_LEN = 4096

    def __init__(self, token, chat_ids, disable_notifications=False, disable_preview=False):
        self.token = token
        self.chat_ids = chat_ids
        self.disable_notifications = disable_notifications
        self.disable_preview = disable_preview
        self.session = requests.Session()
        super().__init__()

    @property
    def url(self):
        return "https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=markdown&" \
               "disable_web_page_preview={disable_web_page_preview}&disable_notifications={disable_notifications}"

    def handle(self, record):

        record = self.format(record)

        if len(record) > self.MAX_MSG_LEN:

            # telegram max length of text is 4096 chars, we need to split our text into chunks

            start_idx, end_idx = 0, self.MAX_MSG_LEN - 2  # don't forget about markdown symbols (```)
            start_chars, end_chars = "", "```"
            new_record = record[start_idx:end_idx]

            while new_record:

                # remove whitespaces, markdown fmt symbols and a carriage return
                new_record = start_chars + new_record.rstrip("` \n") + end_chars
                self.emit(new_record)

                start_chars = end_chars = "```"
                start_idx, end_idx = end_idx, end_idx * 2
                new_record = record[start_idx:end_idx]
        else:
            self.emit(record)

    def emit(self, record):
        for chat_id in self.chat_ids:
            url = self.url.format(
                token=self.token,
                chat_id=chat_id,
                text=record,
                disable_web_page_preview=self.disable_preview,
                disable_notifications=self.disable_notifications
            )

            self.session.get(url, timeout=self.TIMEOUT)

    def __del__(self):
        self.session.close()
