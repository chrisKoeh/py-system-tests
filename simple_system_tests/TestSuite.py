import sys
import argparse
import json

from simple_system_tests.ReportHtml import ReportHtml
from simple_system_tests.CachedLogger import CachedLogger
from simple_system_tests.TestCase import TestCase
from simple_system_tests.TestResult import TestResult
from simple_system_tests.helper import *

global __Suite
global __env_params

def set_env_params(params):
    global __env_params
    __env_params = params

class TestSuite:
    def __init__(self):
        self._report = ReportHtml()
        self.__testcases = []
        self.__pass_counter = 0
        self.__fail_counter = 0
        self.__cmd_options = ["no", "h", "p", "o"]
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument('-no','--no-suite-setup', help='No Suite Prepare and Teardown', action="store_true")
        self.__parser.add_argument('-p','--json-system-params', help='Path to JSON params file.', default="system_params.json")
        self.__parser.add_argument('-o','--report-output', help='Path to report html file.', default="index.html")
        self.__old_stdout = None
        self.__stdout = None
        self.prepare_func = None
        self.teardown_func = None

    def __add_cmd_option(self, desc):
        for cmd_len in range(len(desc)):
            if self.__cmd_options == []:
                cmd_opt = desc[0:1].lower()
                self.__cmd_options.append(cmd_opt)
                return cmd_opt

            duplicate=False
            cmd_opt = desc[0:cmd_len + 1].lower()
            for c in self.__cmd_options:
                if cmd_opt == c:
                    duplicate = True
                    break
            if not duplicate:
                self.__cmd_options.append(cmd_opt)
                return cmd_opt

        raise Exception(desc + " has duplicate description")

    def __fail(self):
        self.__fail_counter = self.__fail_counter + 1
        print("\n\n----\nFAIL\n----\n")

    def __pass(self):
        self.__pass_counter = self.__pass_counter + 1
        print("\n\n----\nPASS\n----\n")

    def __suite(self, no_suite_setup, desc):
        start = get_time()
        if not no_suite_setup:
            test_result = TestResult("Suite " + desc)
            try:
                print(get_overline())
                print("Suite " + desc + "\n")
                self.logger = self.__cached_logger.start_logging()
                if desc == "Setup":
                    self.prepare_func()
                else:
                    self.teardown_func()
                test_result.result = True
            except Exception as ec:
                self.logger.error(get_exception(ec))
                self.logger.error("ABORT: Suite " + desc + " failed")
                test_result.log = self.__cached_logger.stop_logging()
                test_result.duration = get_time() - start
                self._report.add_result(test_result)
                self._report.finish_results(self.__report_file)
                sys.exit(1)

            test_result.log = self.__cached_logger.stop_logging()
            test_result.duration = get_time() - start
            self._report.add_result(test_result)

    def __run_testcase(self, tc):
        tc_desc = tc.get_description()
        print(get_overline())
        print("TEST " + tc_desc + ":\n\n")

        self.logger = self.__cached_logger.start_logging()
        test_result = tc.run_testcase(self.logger)
        test_result.log = self.__cached_logger.stop_logging()

        if test_result.result:
            self.__pass()
        else:
            self.__fail()
        self._report.add_result(test_result)

    def add_test_case(self, test_case, sub_params=[]):
        desc = test_case.get_description()
        test_case.set_sub_params(sub_params)
        desc_cmd = desc.replace(" ", "_").replace("-","_").lower()
        self.__parser.add_argument('-' + self.__add_cmd_option(desc),'--' + desc_cmd, help='Test ' + desc, action="store_true")
        self.__testcases.append(test_case)

    def execute_tests(self):
        def specific_tests_chosen():
            for tc in self.__testcases:
                if tc.is_active(args):
                    return True
            return False

        def read_json_env():
            try:
                params = json.loads(open(params.env).read())
                set_env_params(params)
            except Exception as ec:
                print(str(ec) + ". So no parameters will be passed!")

        def run_testcase_s(tc):
            sub_params = tc.get_sub_params()
            if sub_params != []:
                for i in range(len(sub_params)):
                    tc.set_sub(i)
                    self.__run_testcase(tc)
            else:
                self.__run_testcase(tc)

        self.__cached_logger = CachedLogger()
        args = self.__parser.parse_args()
        no_suite_setup = vars(args)["no_suite_setup"]
        params_env = vars(args)["json_system_params"]
        self.__report_file = vars(args)["report_output"]

        read_json_env()

        if self.prepare_func:
            self.__suite(no_suite_setup, "Setup")

        specific_tests_set = specific_tests_chosen()
        for tc in self.__testcases:
            if specific_tests_set and not tc.is_active(args):
                continue

            run_testcase_s(tc)

        if self.teardown_func:
            self.__suite(no_suite_setup, "Teardown")
        self._report.finish_results(self.__report_file)

        print(get_overline())
        print("Total pass: " + str(self.__pass_counter))
        print("Total fail: " + str(self.__fail_counter))

        if self.__fail_counter != 0:
            sys.exit(1)

def __add_tc(func, sub_params=[], retry=0, timeout=-1, prepare_func=None, teardown_func=None):
    global __Suite
    desc = func.__name__
    desc = desc[0].upper() + desc[1:]
    T=TestCase(desc.replace("_"," "))
    T.retry=retry
    T.timeout=timeout
    T.execute_func = func
    T.prepare_func = prepare_func
    T.teardown_func = teardown_func
    __Suite.add_test_case(T, sub_params)

set_env_params({})
__Suite = TestSuite()

# public functions
def get_env():
    return __env_params

def set_env(key, value):
    global __env_params
    __env_params[key] = value

def prepare_suite(func):
    __Suite.prepare_func = func

def teardown_suite(func):
    __Suite.teardown_func = func

def logger():
    return __Suite.logger

def testcase(retry=0, timeout=-1, prepare_func=None, teardown_func=None):
    def testcase_(func):
        __add_tc(func, [], retry, timeout, prepare_func, teardown_func)
    return testcase_

def testcases(sub_params, retry=0, timeout=-1, prepare_func=None, teardown_func=None):
    def testcases_(func):
        __add_tc(func, sub_params, retry, timeout, prepare_func, teardown_func)
    return testcases_

def run_tests():
    __Suite.execute_tests()
