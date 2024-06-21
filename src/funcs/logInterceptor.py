"""
The idea was to intercept normal logs, and combine them on the fly with omrolocs logs, but this only works for
logs created with python logging module, which, sadly is not the case for a certain large world
"""


import logging


class LogInterceptor(object):
    def __init__(self):
        self.logPath = 'example.log'
        self.logs = []

        self.log_handler = CapturingHandler(self.logs)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(self.log_handler)

    def save(self):
        with open(self.logPath, 'w') as file:
            for log_entry in self.logs:
                file.write(log_entry + '\n')

class CapturingHandler(logging.Handler):
    def __init__(self, logs_list):
        logging.Handler.__init__(self)
        self.logs_list = logs_list

    def emit(self, record):
        log_entry = self.format(record)
        self.logs_list.append(log_entry)

stak = LogInterceptor()
