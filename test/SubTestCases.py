import simple_system_tests as sst
import time

class SubTestCase(sst.TestCase):
    def execute(self):
        print("Test number is: " + str(self.test_params))

class SubDictTestCase(sst.TestCase):
    def execute(self):
        print("Testdict number is: " + str(self.test_params["index"]))

arr = []
arr_dict = []
for i in range(10):
    arr.append(i)
    arr_dict.append({"index":i})

T=sst.TestSuite()
T.add_test_case(SubTestCase("sub testcase"), arr)
T.add_test_case(SubDictTestCase("subdict testcase"), arr_dict)
T.execute_tests()