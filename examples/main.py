import simple_system_tests as sst
import time

@sst.prepare_suite
def custom_suite_prepare(self):
    self.logger.info("Preparing the testSuite")

@sst.teardown_suite
def custom_suite_teardown(self):
    print("Tearing down the testSuite")

@sst.testcase(desc="simple print")
def print_case(self):
    self.logger.info("simple")

@sst.testcase("multi prints", ["1", "2", "3"])
def print_sub_cases(self):
    self.logger.info("multi " + self.test_params)

@sst.testcase("JSON multi prints", [{"name":"Egon"}, {"name":"Kjelt"}])
def print_json_sub_cases(self):
    self.logger.info("JSON multi " + self.test_params["name"])

@sst.testcase("retries", retry=2)
def retry_case(self):
    raise Exception("failed retry")

@sst.testcase("timeouted", timeout=0.5)
def timeout_case(self):
    time.sleep(1)

def custom_testcase_prepare(self):
    self.logger.info("preparing this case")

def custom_testcase_teardown(self):
    self.logger.info("tearing down this case")

@sst.testcase("prepared and torndown", retry=2, prepare_func=custom_testcase_prepare, teardown_func=custom_testcase_teardown)
def prepare_case(self):
    raise Exception("retrying")

sst.run_tests()
