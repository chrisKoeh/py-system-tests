global DROPDOWN_COUNTER
DROPDOWN_COUNTER=0

def style_css_and_js():
    return '''<style>

tr:nth-child(even){background-color: #f2f2f2;}

td {
    padding:10px;
    border: 1px solid grey;
}

.dropbtn {
  background-color: grey;
  color: white;
  padding: 5px;
  border: none;
  cursor: pointer;
}

.dropbtn:hover, .dropbtn:focus {
  background-color: #2980B9;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  padding:10px;
}

.dropdown-content tr td{
  padding:5px;
}

.show {display: block;}
</style>
</head>
<body>

<script>
function show_log(c) {
  document.getElementById("myDropdown" + String(c)).classList.toggle("show");
}
</script>'''

def dropdown_link(log):
    global DROPDOWN_COUNTER
    LOG_OUTS = ["DEBUG", "CRITICAL", "INFO", "WARNING", "ERROR"]
    DROPDOWN_COUNTER = DROPDOWN_COUNTER + 1
    log_lines = log.split("</br>")

    log_content = ""
    for l in log_lines:
        if l == "":
            continue

        log_entries = l.split(" ")
        if len(log_entries) > 3 and log_entries[3] in LOG_OUTS:
            if log_content != "":
                log_content = log_content + "</td></tr>"

            log_content = log_content + "<tr><td><b>" + log_entries[0] + " " + log_entries[1] + "</b></td>"
            log_content = log_content + "<td><b>" + log_entries[3] + "</b></td>"
            log_content = log_content + "<td>" + " ".join(log_entries[5:])
        else:
            log_content = log_content + "</br>" + " ".join(log_entries)

    if log_content != "" and not log_content.endswith("</tr>"):
        log_content = log_content + "</td></tr>"

    return '''<div class="dropdown">
  <button onclick="show_log(''' + str(DROPDOWN_COUNTER) + ''')" class="dropbtn">Log Content</button>
  </div><table id="myDropdown''' + str(DROPDOWN_COUNTER) + '''" class="dropdown-content">''' + log_content + '''
  </table>'''

class ReportHtml(object):
    def __init__(self):
        self.__html = '<!doctype html><html><head><title>System Test Results</title>' + style_css_and_js() + '</head><body><table>'
        self.__html = self.__html + "<tr><td><b>Testcase</b></td><td><b>Log</b></td><td><b>Duration (s)</b></td>"
        self.__html = self.__html + "<td><b>Retries(allowed)</b></td><td><b>Result</b></td></tr>"

    def add_result(self, res):
        duration = '{:.5f}'.format(res.duration)
        color = "red"
        txt = "FAIL"
        if res.result:
            color = "green"
            txt = "PASS"

        log_html = ""
        if res.log.strip() != "":
            log_html = dropdown_link(res.log.replace("\n", "</br>"))
        self.__html = self.__html + '<tr>'
        self.__html = self.__html + '<td>' + res.description + '</td>'
        self.__html = self.__html + '<td style="min-width:600px">' + log_html + '</td>'
        self.__html = self.__html + '<td style="text-align:center">' + str(duration) + '</td>'
        self.__html = self.__html + '<td style="text-align:center">' + str(res.retry) + '(' + str(res.retry_allowed) + ')</td>'
        self.__html = self.__html + '<td style="text-align:center;color:white;background-color:'
        self.__html = self.__html + color + '">' + txt + '</td>'
        self.__html = self.__html + "</tr>"

    def finish_results(self, output_file):
        self.__html = self.__html + "</table></body></html>"
        open(output_file, "w").write(self.__html)
