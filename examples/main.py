import simple_system_tests as sst
import time

@sst.prepare_suite
def custom_suite_prepare():
    sst.logger().info("Preparing the testSuite")
    sst.set_env("env1", 5)

@sst.teardown_suite
def custom_suite_teardown():
    print("Tearing down the testSuite")

@sst.testcase()
def env_case():
    sst.logger().warning(sst.get_env())

@sst.testcase()
def simple_print():
    sst.logger().info("simple")

@sst.testcases(["1", "2", "3"])
def multi_prints(s):
    sst.logger().info(s)

@sst.testcases([{"name":"Egon"}, {"name":"Kjeld"}, {"name":"Benny"}])
def json_multi_prints(j):
    sst.logger().info("JSON multi " + j["name"])

@sst.testcase(retry=2)
def retry_case():
    raise Exception("failed retry")

@sst.testcase(timeout=0.5)
def timeout_case():
    time.sleep(1)

def custom_testcase_prepare():
    sst.logger().info("preparing this case")

def custom_testcase_teardown():
    sst.logger().info("tearing down this case")

@sst.testcase(retry=2, prepare_func=custom_testcase_prepare, teardown_func=custom_testcase_teardown)
def prepare_case():
    raise Exception("retrying")

sst.run_tests()
