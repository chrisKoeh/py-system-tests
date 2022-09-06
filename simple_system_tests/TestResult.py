class TestResult(object):
    def __init__(self, desc):
        self.result = False
        self.retry = 0
        self.retry_allowed = 0
        self.description = desc
        self.log = ""
        self.duration = 0.0
