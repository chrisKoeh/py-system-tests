# simple-system-tests
Simple Python library for writing test cases for System and components tests including automatic reports via html.
## Installation
The module is currently not published on pypi, so has to built manually:
```
pip3 install setuptools wheel
python3 setup.py sdist bdist_wheel
(sudo) python3 setup.py install
```
## Quick-Start
Go to `examples` and run:
```
python3 main.py
```
which will execute two testcases (defined under `examples/GoogleTestCase.py` and `examples/TimeTestCase.py`). After that open the created `examples/index.html` for an overview of the results in a web browser.
## Testsuite
The Testsuite is defined under `simple_system_tests/TestSuite.py`:
- holds testcases
- prepares and teardown of Testsuite, which can be implemented by deriving a new class from it and overwriting the `prepare` and `teardown` functions, eg:
```
class CustomTestSuite(TestSuite):
    def prepare(self):
        subprocess.run("ip link set dev eth0 up", shell=True)
```
- reporting of test results stored in `index.html`
- providing command line options for all testcases and some fixed ones

## Command line options
When using a Testsuite command line options for all testcases added to the suite will be automatically added. command line option shortcut will be derived from the beginning characters of the description string passed to the testcase. So make sure to have varying descriptions for your testcases. Having a look at the help of `examples/main.py` again will give the following output:
```
shell: python3 main.py -h
usage: main.py [-h] [-no] [-p JSON_SYSTEM_PARAMS] [-o REPORT_OUTPUT] [-ht] [-ho]

optional arguments:
  -h, --help            show this help message and exit
  -no, --no-suite-setup
                        No Suite Prepare and Teardown
  -p JSON_SYSTEM_PARAMS, --json-system-params JSON_SYSTEM_PARAMS
                        Path to JSON params file.
  -o REPORT_OUTPUT, --report-output REPORT_OUTPUT
                        Path to report html file.
  -ht, --Http get to google via IPv6 and IPv4
                        Test Http get to google via IPv6 and IPv4
  -ho, --Host unix time
                        Test Host unix time
```
So testcases can be called separately without having to execute all testcases in one run. It is also possible to pass multiple testcases in one execution. In case the Suite setup and teardown is not wanted this can be achieved by putting the `-no, --no-suite-setup` option.
## Testcases
### Create new testcases
Testcases need to be derived from the base Testcase class(`simple_system_tests/Testcase.py`), by overwriting the:
- prepare (optional)
- execute (required)
- teardown (optional)

functions.A testcase is considered a `PASS` as long as no exception is raised. For example:
```
class CustomTestCase(TestCase):
    def execute(self):
        raise Exception("Fails always, anyways")
```
Upon Object creation a description needs to be passed to the Testcase:
```
t = CustomTestCase("Always failing task")
```
### System parameters
Environment parameters for the testsuite can be used from a json file named `system_params.json` (the file path can be customized by passing the `-p` option). Those will be made available in the Testcase by the attribute `self.params`:
```
class CustomTestCase(TestCase):
    def execute(self):
        self.logger.info(self.params["key_from_sys_params"])
        raise Exception("Fails always, anyways")
```
It is also possible to access and modify this attribute from within the testsuite, eg. in case a global python object should be made available in Testsuite preparation for all testcases.
### Logging
The file path of the output file can be customized by passing the `-o` option, defaults to `index.html`. A `logger` object attribute is available within testcases and testsuites, eg:
```
class CustomTestSuite(TestSuite):
    def prepare(self):
        self.logger.info("Preparing the test suite")
```
However stdout is mapped to `logger.info`, hence `print` can also be used directly which will result in output of both console and html report file.