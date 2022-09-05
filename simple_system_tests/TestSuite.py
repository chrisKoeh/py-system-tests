import sys
from io import StringIO
import argparse
import json
import os
import datetime
import traceback

from simple_system_tests.ReportHtml import ReportHtml
from simple_system_tests.CachedLogger import CachedLogger
from simple_system_tests.TestCase import TestCase

DEFAULT_OVERLINE_COLS=60

global __Suite
global __env_params

def get_overline():
    cols = DEFAULT_OVERLINE_COLS
    try:
        cols = os.get_terminal_size().columns
    except:
        pass

    ol = ""
    for _ in range(cols):
        ol = ol + "_"
    return ol + "\n"

def set_env_params(params):
    global __env_params
    __env_params = params

def log_exception(ec):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    last = len(tb_lines) - 1
    logger().error(tb_lines[last - 1] + tb_lines[last])

def get_time():
    return datetime.datetime.now().timestamp()

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
            try:
                print(get_overline())
                print(desc + " of Suite\n")
                self.logger = self.__cached_logger.start_logging()
                if desc == "Setup":
                    self.prepare_func()
                else:
                    self.teardown_func()
            except Exception as ec:
                log_exception(ec)
                self.logger.error("ABORT: Suite " + desc + " failed")
                self._report.add_result("Suite " + desc, self.__cached_logger.stop_logging(), False, get_time() - start, [0,0])
                self._report.finish_results(self.__report_file)
                sys.exit(1)

            self._report.add_result("Suite " + desc, self.__cached_logger.stop_logging(), True, get_time() - start, [0,0])

    def __run_testcase(self, tc):
        def __perform_task(func, desc):
            start = get_time()
            try:
                func()
                return [True, get_time() - start]
            except Exception as ec:
                log_exception(ec)
                self.logger.error(desc + " failed.")
                tc_failed = True
                return [False, get_time() - start]

        def __execute():
            [res, duration] = __perform_task(tc.execute, "Testcase")
            if tc.timeout > 0:
                if tc.timeout < duration:
                    self.logger.error("Testcase execution timeout (" + str(tc.timeout) + " s) exceeded taking " + '{:.5f}'.format(duration) + " s instead.")
                    res = False

            return [not res, duration]

        tc_failed = True
        tc_desc = tc.get_description()
        print(get_overline())
        print("TEST " + tc_desc + ":\n\n")
        self.logger = self.__cached_logger.start_logging()
        tc.logger = self.logger

        [res, duration] = __perform_task(tc.prepare, "Preparation of testcase")
        if not res:
            self._report.add_result(tc_desc, self.__cached_logger.stop_logging(), False, duration, [0,0])
            self.__fail()
            return

        retries = -1
        while retries < tc.retry and tc_failed:
            retries = retries + 1
            if retries > 0:
                self.logger.info(str(retries) + ". Retry of testcase now.")
            tc_failed, duration = __execute()

        [teardown_res, _] = __perform_task(tc.teardown, "Testcase teardown")

        log = self.__cached_logger.stop_logging()
        res = not tc_failed and teardown_res
        if res:
            self.__pass()
        else:
            self.__fail()

        self._report.add_result(tc_desc, log, res, duration, [retries, tc.retry])

    def add_test_case(self, test_case, sub_params=[]):
        desc = test_case.get_description()
        test_case.set_sub_params(sub_params)
        desc_cmd = desc.replace(" ", "_").replace("-","_").lower()
        self.__parser.add_argument('-' + self.__add_cmd_option(desc),'--' + desc_cmd, help='Test ' + desc, action="store_true")
        self.__testcases.append(test_case)

    def execute_tests(self):
        self.__cached_logger = CachedLogger()
        args = self.__parser.parse_args()
        no_suite_setup = vars(args)["no_suite_setup"]
        params_env = vars(args)["json_system_params"]
        self.__report_file = vars(args)["report_output"]

        try:
            params = json.loads(open(params_env).read())
            set_env_params(params)
        except Exception as ec:
            print(str(ec) + ". So no parameters will be passed!")

        all_inactive = True
        for tc in self.__testcases:
            if tc.is_active(args):
                all_inactive = False
                break

        if self.prepare_func:
            self.__suite(no_suite_setup, "Setup")

        for tc in self.__testcases:
            if not all_inactive and not tc.is_active(args):
                continue

            sub_params = tc.get_sub_params()
            if sub_params != []:
                for i in range(len(sub_params)):
                    tc.set_sub(i)
                    self.__run_testcase(tc)
            else:
                self.__run_testcase(tc)

        if self.teardown_func:
            self.__suite(no_suite_setup, "Teardown")
        self._report.finish_results(self.__report_file)

        print(get_overline())
        print("Total pass: " + str(self.__pass_counter))
        print("Total fail: " + str(self.__fail_counter))

        if self.__fail_counter != 0:
            sys.exit(1)

set_env_params({})
__Suite = TestSuite()

# public functions except for __add_tc
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
