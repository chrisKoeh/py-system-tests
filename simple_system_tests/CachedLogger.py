import logging
import io
import sys

class LoggerWriter:
    def __init__(self, logfct):
        self.__logfct = logfct
        self.__buf = []

    def write(self, msg):
        if msg.endswith('\n'):
            self.__buf.append(msg.strip('\n'))
            self.__logfct(''.join(self.__buf))
            self.__buf = []
        else:
            self.__buf.append(msg)

class CachedLogger(object):
    def __init__(self):
        self.__log_capture_string = io.StringIO()
        ch = logging.StreamHandler(self.__log_capture_string)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.__logger = logging.getLogger('basic_logger')
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.addHandler(ch)

    def start_logging(self):
        self.__old_stdout = sys.stdout
        self.__old_stderr = sys.stderr
        sys.stdout = LoggerWriter(self.__logger.info)
        sys.stderr = LoggerWriter(self.__logger.error)
        return self.__logger

    def stop_logging(self):
        log_contents = self.__log_capture_string.getvalue()
        self.__log_capture_string.flush()
        self.__log_capture_string.seek(0)
        self.__log_capture_string.truncate(0)
        sys.stdout = self.__old_stdout
        sys.stderr = self.__old_stderr
        print(log_contents)
        return log_contents

    def __del__(self):
        self.__log_capture_string.close()
