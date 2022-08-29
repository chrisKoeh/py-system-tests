import simple_system_tests as sst

class SetupFail(sst.TestSuite):
    def prepare(self):
        raise Exception("failed")

T=SetupFail()
T.execute_tests()
