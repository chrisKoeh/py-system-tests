import requests
import datetime

import simple_system_tests as sst

UNIX_URL="https://unixtimestamp.com"

class TimeTestCase(sst.TestCase):
    def execute(self):
        self.logger.info("Get current timestamp...")
        current_time = int(datetime.datetime.now().timestamp())
        self.logger.info(str(current_time))

        self.logger.info("Get timestamp from " + UNIX_URL + "...")
        pattern = '<div class="value epoch">'
        r = requests.get(UNIX_URL)
        found_stamp_raw = r.text[r.text.find('<div class="value epoch">') + len(pattern):]
        found_stamp = int(found_stamp_raw[0:found_stamp_raw.find("</div>")].strip())
        self.logger.info(str(found_stamp))
        assert(abs(found_stamp-current_time) < 5 )
