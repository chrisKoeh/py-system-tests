import requests

import simple_system_tests as sst

class GoogleTestCase(sst.TestCase):
    def execute(self):
        self.logger.info("Test IPv4 access to Google...")
        requests.get("https://" + self.params["v4google"])

        self.logger.info("Test IPv6 access to Google...")
        requests.get("https://" + self.params["v6google"])
