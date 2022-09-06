from html.parser import HTMLParser

class HtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__start_tag = False
        self.__data = []
        self.__data_p = 5
    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.__start_tag = True
    def handle_data(self, data_):
        if self.__start_tag:
            self.__data.append(data_)

        self.__start_tag = False
    def validate(self, exp_desc, exp_log=[], exp_duration=0.0,
                          exp_retries="0(0)", exp_res="PASS", log_count=1, exp_not=""):

        data = self.__data
        print("Unit test: " + exp_desc)
        if exp_not:
            complete_s = "\n".join(data[self.__data_p: self.__data_p + 5 + (3*log_count)])
            assert exp_not not in complete_s

        assert data[self.__data_p] == exp_desc
        if exp_log != []:
            assert data[self.__data_p+3] == exp_log[0]
            assert data[self.__data_p+4].startswith(exp_log[1])

        self.__data_p = self.__data_p + 2 + (3*log_count)
        duration = float(data[self.__data_p])
        assert exp_duration < duration
        assert exp_duration + 0.1 > duration
        assert exp_retries == data[self.__data_p+1]
        assert exp_res == data[self.__data_p+2]
        self.__data_p = self.__data_p + 3
        print("PASS")
