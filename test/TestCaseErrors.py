import simple_system_tests as sst
import time

class TimeoutTestCase(sst.TestCase):
    def execute(self):
        self.timeout = 0.5
        time.sleep(1)

class RetryTestCase(sst.TestCase):
    def execute(self):
        self.retry = 2
        raise Exception("Failed retries")

T=sst.TestSuite()
T.add_test_case(TimeoutTestCase("timeout testcase"))
T.add_test_case(RetryTestCase("retry testcase"))
T.execute_tests()