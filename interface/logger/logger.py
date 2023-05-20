#
# ログを記録する責務
#

import logging


class Logger():
    def __init__(self, homedir):
        self.homedir = homedir

    def getLogger(self):
        # set logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        log_fmt = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        log_handler = logging.FileHandler(
            self.homedir + '/.slack-hotkey/slack-hotkey.log'
        )
        log_handler.setFormatter(log_fmt)
        logger.addHandler(log_handler)
        return logger
