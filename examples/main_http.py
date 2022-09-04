from simple_system_tests import *
import requests  # pip3 install requests

testcases_ = [("gmx.net", 200, "GET"),
              ("google.de", 405, "POST"),
              ("gmx.net/roflfoobar", 404, "GET")]

@testcases(testcases_)
def check_status_code(url_params):
    url = url_params[0]
    expected_code = url_params[1]
    method = url_params[2]
    r = requests.request(method, "https://" + url)
    print(r.status_code)
    assert expected_code == r.status_code

run_tests()
