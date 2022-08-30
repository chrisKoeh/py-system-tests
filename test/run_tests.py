import subprocess

import simple_system_tests as sst

SUCCESS="SUCCESS"

def shell_call(cmd):
    r=subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return [r.stdout.decode("utf-8"), r.stderr.decode("utf-8")]

def test_suite(script, err_desc, kind):
    r = shell_call("python3 " + script + " || echo " + SUCCESS)
    report = open("index.html").read()
    if not SUCCESS in r[0] or not err_desc in r[0] or not err_desc in report:
        print(kind + " error")

shell_call("cd ..; python3 setup.py bdist_wheel sdist; python3 setup.py install")
test_suite("SuiteTearDownFails.py", "ERROR - ABORT: Suite Teardown failed", "Suite teardown")
test_suite("SuiteSetupFails.py", "ERROR - ABORT: Suite Setup failed", "Suite setup")

r = shell_call("python3 TestCaseErrors.py || echo " + SUCCESS)
report = open("index.html").read()
if not SUCCESS in r[0]:
    print("Testcase error, no " + SUCCESS + " found")

if not "Testcase execution timeout" in open("index.html").read():
    print("Testcase timeout error")

if not "Failed retries" in report or not "2(2)" in report:
    print("Testcase retries error")