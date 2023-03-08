# Execute before: echo '{"env0":"str"}' > system_params.json; python3 examples/main.py > log
# Preferred way to call: python3 tests/pseudo_unit_tests.py

import subprocess
import sys

from HtmlParser import HtmlParser
from LogParser import LogParser

log_parser = LogParser("log")
html_parser = HtmlParser()
html_parser.feed(open("index.html").read().replace("<pre>", "").replace("</pre>", ""))

def validate_testcase(exp_desc, exp_log=[], exp_duration=0.0,
                          exp_retries="0(0)", exp_res="PASS", log_count=1, exp_not=""):

    html_parser.validate(exp_desc, exp_log, exp_duration, exp_retries, exp_res, log_count, exp_not)
    log_parser.validate(exp_desc, exp_log, exp_res)

def validate_readme():
    print("Unit test: validate that examples/main.py help is found in README.md.")
    help=subprocess.check_output("python3 examples/main.py -h", shell=True).decode("utf-8")
    readme=open("README.md").read()
    help_readme = readme[readme.find("usage: main.py"):]
    help_readme = help_readme[:help_readme.find("```")].replace("optional arguments", "options")
    help = help.replace("optional arguments", "options")
    if help != help_readme:
        raise Exception("Help in README.md differs")
    print("PASS")

json_env = "{'env0': 'str', 'env1': 5}"
suite_setup = True
if len(sys.argv) > 1:
    if sys.argv[1] == "-no":
        suite_setup = False
        json_env = "{'env0': 'str'}"

if suite_setup:
    validate_testcase("Suite Setup", ["INFO", "Preparing the testSuite"])
validate_testcase("Env case", ["WARNING", json_env])
validate_testcase("Simple print", ["INFO", "simple"])
for i in range(3):
    validate_testcase("Multi prints - " + str(i+1), ["INFO", str(i+1)])

for n in ["Egon", "Kjeld", "Benny"]:
    validate_testcase("Json multi prints - name:" + n, ["INFO", "JSON multi " + n])

validate_testcase("Retry case", exp_retries="2(2)", exp_res="FAIL", log_count=8)
validate_testcase("Timeout case", ["ERROR", "Testcase execution timeout"], exp_duration=1.0, exp_res="FAIL")
validate_testcase("Prepare fail case", exp_res="FAIL", log_count=2, exp_not="This wont be printed")
validate_testcase("Teardown fail case", ["INFO", "This will be printed"], exp_res="FAIL", log_count=3)
if suite_setup:
    validate_testcase("Suite Teardown", ["INFO", "Tearing down the testSuite"])
validate_readme()
