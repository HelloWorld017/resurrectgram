import logging
import traceback

from signalepy import Signale

class Logger(object):
    def __init__(self):
        self.logger = Signale({
            "scope": "Resurrectgram",
            "custom": [
                {
                    "badge": "\u2237",
                    "label": "Progress",
                    "color": "magenta",
                    "name": "progress"
                },

                {
                    "badge": "\u2715",
                    "label": "Fatal",
                    "color": "red",
                    "name": "fatal"
                }
            ]
        })

        file_handler = logging.FileHandler(filename="./resurrectgram.log")
        file_handler.setFormatter(logging.Formatter("[%(levelname)s] %(asctime)s > %(message)s"))

        self.file_logger = logging.getLogger()
        self.file_logger.propagate = False
        self.file_logger.setLevel(0)
        self.file_logger.addHandler(file_handler)

    def complete(self, text):
        self.logger.complete(text)
        self.file_logger.info("COMPLETE\t" + text)

    def success(self, text):
        self.logger.success(text)
        self.file_logger.info("SUCCESS\t" + text)

    def progress(self, text):
        self.logger.progress(text)
        self.file_logger.info("PROGRESS\t" + text)

    def info(self, text):
        self.logger.info(text)
        self.file_logger.info("INFO\t\t" + text)

    def error(self, error_string, error):
        error_traceback = traceback.format_exception(error.__class__, error, error.__traceback__)
        traceback_lines = []
        for line in [line.rstrip('\n') for line in error_traceback]:
            traceback_lines.extend(line.splitlines())

        self.logger.error(error_string)
        self.file_logger.error("ERROR\t\t" + "\n".join(traceback_lines))

    def fatal(self, text):
        self.logger.fatal(text)
        self.file_logger.critical("FATAL\t\t" + text)
