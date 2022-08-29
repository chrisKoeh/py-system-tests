import simple_system_tests as sst

class TeardownFail(sst.TestSuite):
    def teardown(self):
        raise Exception("failed")

T=TeardownFail()
T.execute_tests()
