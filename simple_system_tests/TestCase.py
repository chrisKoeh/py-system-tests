from simple_system_tests.helper import get_exception, get_time
from simple_system_tests.TestResult import TestResult

class TestCase(object):
    def __init__(self, desc):
        self.__desc = desc
        self.timeout = -1
        self.retry = 0
        self.__sub_desc = ""
        self.__sub_params = []
        self.__current_sub = {}
        self.execute_func = None
        self.prepare_func = None
        self.teardown_func = None
        self.__logger = None
    def __prepare(self):
        if self.prepare_func:
            self.prepare_func()
    def __execute(self):
        if not self.execute_func:
            raise Exception("Not implemented.")
        if self.__sub_params == []:
            self.execute_func()
        else:
            self.execute_func(self.__current_sub)
    def __teardown(self):
        if self.teardown_func:
            self.teardown_func()
    def set_sub_params(self, params):
        if not isinstance(params, list):
            raise Exception("Subtest parameters needs to be of type list.")
        self.__sub_params = params
    def get_sub_params(self):
        return self.__sub_params
    def get_description(self):
        if self.__sub_desc != "":
            return self.__sub_desc
        return self.__desc
    def set_sub(self, i):
        p = self.__sub_params[i]
        suffix = ""
        if isinstance(p, dict):
            for k in p:
                if suffix == "":
                    suffix = k + ":" + str(p[k])
                else:
                    suffix = suffix + ", " + k + ":" + str(p[k])
        else:
            suffix = str(p)
        self.__sub_desc = self.__desc + " - " + suffix
        self.__current_sub = p
    def __perform_task(self, func, task_desc):
        try:
            func()
            return True
        except Exception as ec:
            self.__logger.error(get_exception(ec))
            self.__logger.error(task_desc + " failed.")
            return False
    def run_testcase(self, logger):
        self.__logger = logger
        test_result = TestResult(self.get_description())
        start_prepare = get_time()
        res = self.__perform_task(self.__prepare, "Preparation of testcase")
        if not res:
            test_result.result = False
            test_result.duration = get_time() - start_prepare
            return test_result

        test_result.retry = -1
        test_result.retry_allowed = self.retry
        while test_result.retry < test_result.retry_allowed and not test_result.result:
            test_result.retry += 1
            if test_result.retry > 0:
                self.__logger.info(str(test_result.retry) + ". Retry of testcase.")
            start = get_time()
            test_result.result = self.__perform_task(self.__execute, "Testcase")
            test_result.duration = get_time() - start
            if test_result.duration > self.timeout and self.timeout > 0:
                self.__logger.error("Testcase execution timeout (" + str(self.timeout) +" s) exceeded taking " + '{:.5f}'.format(test_result.duration) + " s instead.")
                test_result.result = False

        res = self.__perform_task(self.__teardown, "Testcase teardown")
        test_result.result = res and test_result.result
        return test_result

    def is_active(self, args):
       active = vars(args)[self.__desc.replace("-","_").replace(" ", "_").lower()]
       return active
    def __del__(self):
       pass
