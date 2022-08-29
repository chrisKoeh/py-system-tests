import sys
from io import StringIO
import argparse
import json

from simple_system_tests.ReportHtml import ReportHtml
from simple_system_tests.CachedLogger import CachedLogger

PARAMS_ENV = "system_params.json"
REPORT_OUTPUT="index.html"
OVERLINE="---------------------------------------------------------------------\n"

class TestSuite:
    def __init__(self):
        self._report = ReportHtml()
        self.__testcases = []
        self.__pass_counter = 0
        self.__fail_counter = 0
        self.__cmd_options = ["no", "h", "p", "o"]
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument('-no','--no-suite-setup', help='No Suite Prepare and Teardown', action="store_true")
        self.__parser.add_argument('-p','--json-system-params', help='Path to JSON params file.', default=PARAMS_ENV)
        self.__parser.add_argument('-o','--report-output', help='Path to report html file.', default=REPORT_OUTPUT)
        self.params = {}
        self.__old_stdout = None
        self.__stdout = None

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
        if not no_suite_setup:
            try:
                print(OVERLINE)
                print(desc + " of Suite\n")
                self.logger = self.__cached_logger.start_logging()
                if desc == "Setup":
                    self.prepare()
                else:
                    self.teardown()
            except Exception as ec:
                self.logger.error("ABORT: Suite " + desc + " failed with " + str(ec))
                self._report.add_result("Suite " + desc, self.__cached_logger.stop_logging(), False)
                self._report.finish_results(self.__report_file)
                sys.exit(1)

            self._report.add_result("Suite " + desc, self.__cached_logger.stop_logging(), True)

    def __run_testcase(self, tc):
            tc.set_params(self.params)

            print(OVERLINE)
            print("TEST " + tc.get_description() + ":\n\n")
            tc_failed = False
            self.logger = self.__cached_logger.start_logging()
            tc.logger = self.logger
            try:
                tc.prepare()
            except Exception as ec:
                self.logger.error("Preparation of testcase failed with: " + str(ec))
                self._report.add_result(tc.get_description(), self.__cached_logger.stop_logging(), False)
                self.__fail()
                return

            try:
                tc.execute()
            except Exception as ec:
                self.logger.error("Testcase execution failed with: " + str(ec))
                tc_failed = True

            try:
                tc.teardown()
            except Exception as ec:
                self.logger.error("Testcase teardown failed with: " + str(ec))
                tc_failed = True

            log = self.__cached_logger.stop_logging()
            if not tc_failed:
                self.__pass()
            else:
                self.__fail()
            
            self._report.add_result(tc.get_description(), log, not tc_failed)

    def prepare(self):
        pass

    def teardown(self):
        pass

    def add_test_case(self, test_case):
        desc = test_case.get_description()
        self.__parser.add_argument('-' + self.__add_cmd_option(desc),'--' + desc, help='Test ' + desc, action="store_true")
        self.__testcases.append(test_case)

    def execute_tests(self):
        self.__cached_logger = CachedLogger()
        args = self.__parser.parse_args()
        no_suite_setup = vars(args)["no_suite_setup"]
        params_env = vars(args)["json_system_params"]
        self.__report_file = vars(args)["report_output"]

        try:
            self.params = json.loads(open(params_env).read())
        except Exception as ec:
            print(str(ec) + ". So no parameters will be passed!")
            self.params = {}

        all_inactive = True
        for tc in self.__testcases:
            if tc.is_active(args):
                all_inactive = False
                break

        self.__suite(no_suite_setup, "Setup")

        for tc in self.__testcases:
            if not all_inactive and not tc.is_active(args):
                continue

            self.__run_testcase(tc)

        self.__suite(no_suite_setup, "Teardown")
        self._report.finish_results(self.__report_file)

        print(OVERLINE)
        print("Total pass: " + str(self.__pass_counter))
        print("Total fail: " + str(self.__fail_counter))

        if self.__fail_counter != 0:
            sys.exit(1)
