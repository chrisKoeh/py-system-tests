import subprocess

SUCCESS="SUCCESS"

def shell_call(cmd):
    r=subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return [r.stdout.decode("utf-8"), r.stderr.decode("utf-8")]

def test_suite(script, err_desc, kind):
    r = shell_call("python3 " + script + " || echo " + SUCCESS)
    report = open("index.html").read()
    if not SUCCESS in r[0] or not err_desc in r[0] or not err_desc in report:
        print(kind + " error")

test_suite("SuiteTearDownFails.py", "ERROR - ABORT: Suite Teardown failed", "Suite teardown")
test_suite("SuiteSetupFails.py", "ERROR - ABORT: Suite Setup failed", "Suite setup")