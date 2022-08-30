import simple_system_tests as sst
from HttpGetTestCase import HttpGetTestCase
from TimeTestCase import TimeTestCase

def custom_suite_prepare(self):
    self.logger.info("Preparing the testSuite")

def custom_suite_teardown(self):
    # self.logger.info and print have the same effect
    print("Tearing down the testSuite")

# (Optional) Can be left out or also be achieved by deriving a new class
sst.TestSuite.prepare = custom_suite_prepare
sst.TestSuite.teardown = custom_suite_teardown

T=sst.TestSuite()
T.add_test_case(HttpGetTestCase("Http get"), [
    {"host":"ipv6.google.com", "redundant_param":5},
    {"host":"ipv4.google.com", "redundant_param":3},
    {"host":"gmx.net", "redundant_param":2},
    {"host":"github.com", "redundant_param":4}
])
T.add_test_case(TimeTestCase("Host unix time"))
T.execute_tests()
