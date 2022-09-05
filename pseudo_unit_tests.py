from html.parser import HTMLParser

start_tag = False
global data, data_pointer
data = []
data_p = 5

def validate(exp_desc, exp_log=[], exp_duration=0.0,
                          exp_retries="0(0)", exp_res="PASS", log_count=1, exp_not=""):

    global data
    global data_p
    print("Unit test: " + exp_desc)
    if exp_not:
        complete_s = "\n".join(data[data_p: data_p + 5 + (3*log_count)])
        assert exp_not not in complete_s

    assert data[data_p] == exp_desc
    if exp_log != []:
        assert data[data_p+3] == exp_log[0]
        assert data[data_p+4].startswith(exp_log[1])

    data_p = data_p + 2 + (3*log_count)
    duration = float(data[data_p])
    assert exp_duration < duration
    assert exp_duration + 0.1 > duration
    assert exp_retries == data[data_p+1]
    assert exp_res == data[data_p+2]
    data_p = data_p + 3
    print("PASS")

class HtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global start_tag
        if tag == "td":
            start_tag = True
    def handle_data(self, data_):
        global start_tag
        global data

        if start_tag:
            data.append(data_)

        start_tag = False

parser = HtmlParser()
parser.feed(open("index.html").read())

validate("Suite Setup", ["INFO", "Preparing the testSuite"])
validate("Env case", ["WARNING", "{'env1': 5}"])
validate("Simple print", ["INFO", "simple"])
for i in range(3):
    validate("Multi prints - " + str(i+1), ["INFO", str(i+1)])

for n in ["Egon", "Kjeld", "Benny"]:
    validate("Json multi prints - name:" + n, ["INFO", "JSON multi " + n])

validate("Retry case", exp_retries="2(2)", exp_res="FAIL", log_count=8)
validate("Timeout case", ["ERROR", "Testcase execution timeout"], exp_duration=1.0, exp_res="FAIL")
validate("Prepare fail case", exp_res="FAIL", log_count=2, exp_not="This wont be printed")
validate("Teardown fail case", ["INFO", "This will be printed"], exp_res="FAIL", log_count=3)
validate("Suite Teardown", ["INFO", "Tearing down the testSuite"])
