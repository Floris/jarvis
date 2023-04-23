import logging


# Define a custom log record class with color support
class ColoredLogRecord(logging.LogRecord):
    COLOR_MAP = {
        logging.DEBUG: "\x1b[32m",  # Green
        logging.INFO: "\x1b[34m",  # Blue
        logging.WARNING: "\x1b[33m",  # Yellow
        logging.ERROR: "\x1b[31m",  # Red
        logging.CRITICAL: "\x1b[35m",  # Magenta
    }
    RESET_SEQ = "\x1b[0m"

    def getMessage(self) -> str:
        msg = super().getMessage()
        color = self.COLOR_MAP.get(self.levelno, "")
        return f"{color}{msg}{self.RESET_SEQ}"
