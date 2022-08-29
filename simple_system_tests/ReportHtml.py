global DROPDOWN_COUNTER
DROPDOWN_COUNTER=0

def style_css_and_js():
    return '''<style>

tr:nth-child(even){background-color: #f2f2f2;}

th {
  padding-top: 12px;
  padding-bottom: 12px;
  text-align: left;
  background-color: #04AA6D;
  color: white;
}
td {
    padding:20px;
}
.dropbtn {
  background-color: #04AA6D;
  color: white;
  padding: 16px;
  font-size: 16px;
  border: none;
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
  position: absolute;
  padding:10px;
  background-color: #f1f1f1;
  min-width: 900px;
  overflow: auto;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown a:hover {background-color: #ddd;}

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
    DROPDOWN_COUNTER = DROPDOWN_COUNTER + 1
    return '''<div class="dropdown">
  <button onclick="show_log(''' + str(DROPDOWN_COUNTER) + ''')" class="dropbtn">Log Content</button>
  <div id="myDropdown''' + str(DROPDOWN_COUNTER) + '''" class="dropdown-content">''' + log + '''
  </div>
</div>'''

class ReportHtml(object):
    def __init__(self):
        self.html = '<!doctype html><html><head><title>System Test Results</title>' + style_css_and_js() + '</head><body><table>'

    def add_result(self, description, log, result):
        color = "red"
        txt = "FAIL"
        if result:
            color = "green"
            txt = "PASS"

        log_html = ""
        if log.strip() != "":
            log_html = dropdown_link(log.replace("\n", "</br>"))
        self.html = self.html + '<tr>'
        self.html = self.html + '<td><b>' + description + '</b></td>'
        self.html = self.html + '<td>' + log_html + '</td>'
        self.html = self.html + '<td style="color:white;background-color:' + color + '">' + txt + '</td>'
        self.html = self.html + "</tr>"

    def finish_results(self, output_file):
        self.html = self.html + "</table></body></html>"
        open(output_file, "w").write(self.html)