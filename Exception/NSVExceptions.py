

class LogFileWriteError(Exception):
    def __init__(self, _msg):
        self.msg = _msg
