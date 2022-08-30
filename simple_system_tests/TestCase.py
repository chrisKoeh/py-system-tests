class TestCase(object):
    def __init__(self, desc):
        self.__desc = desc
        self.params = {}
        self.logger = None
        self.timeout = -1
        self.retry = 0
    def prepare(self):
        pass
    def execute(self):
        raise Exception("Not implemented.")
    def teardown(self):
        pass
    def get_description(self):
        return self.__desc
    def set_params(self, params):
        self.params = params
    def is_active(self, args):
       active = vars(args)[self.__desc.replace("-","_").replace(" ", "_").lower()]
       return active
    def __del__(self):
       pass
