import logging
from html import escape


__all__ = ("MarkdownFormatter", "HTMLFormatter")


class BaseFormatter(logging.Formatter):

    FMT = BLOCK_OPEN = BLOCK_CLOSE = None

    def __init__(self, fmt: str=None, *args, **kwargs):
        super().__init__(fmt or self.FMT, *args, **kwargs)

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

        record.exc = "{block_open}{exc}{block_close}".format(
            block_open=self.BLOCK_OPEN, exc=record.exc, block_close=self.BLOCK_CLOSE
        ) if record.exc else ""

        return record


class MarkdownFormatter(BaseFormatter):
    """
    Markdown formatter for telegram
    """

    FMT = """*%(levelname)s*\n_%(name)s:%(funcName)s_
    ``` %(message)s ``` %(exc)s
    """

    BLOCK_OPEN = BLOCK_CLOSE = "```"
    MODE = "markdown"


class HTMLFormatter(BaseFormatter):
    FMT = """<b>%(levelname)s</b>\n<i>%(name)s:%(funcName)s</i>
    <pre>%(message)s</pre> %(exc)s
    """

    BLOCK_OPEN = "<pre>"
    BLOCK_CLOSE = "</pre>"
    MODE = "html"

    def format(self, record):
        """
        Properly escape all the string values of message
        """
        for key, value in record.__dict__.items():
            if isinstance(value, str):
                setattr(record, key, escape(value))
        return super().format(record)
