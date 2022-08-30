import requests

import simple_system_tests as sst

class HttpGetTestCase(sst.TestCase):
    def execute(self):
        self.timeout = 0.15
        self.retry = 1

        host = self.test_params["host"]
        self.logger.info("Test access to " + host)
        r = requests.get("https://" + host)
        assert(r.status_code == 200)