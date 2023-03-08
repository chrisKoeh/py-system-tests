import datetime

OVERLINE="_______\n\n"
PASS_LINE="----\n"

def get_current_year():
    d = datetime.datetime.now()
    return d.strftime("%Y")

class LogParser(object):
    def __init__(self, file_name):
        self.__content = open(file_name).read()
        self.__entries = []
        self.__entry_p = 0
        self.__content_p = 0

        while True:
            entry = self.__parse_entry()
            if entry == {}:
                break
            self.__entries.append(entry)

    def __parse_entry(self):
        find_line = self.__content.find(OVERLINE)
        if find_line == -1:
            return {}

        self.__content_p = find_line + len(OVERLINE)
        self.__content = self.__content[self.__content_p:]
        entry_content = self.__content[:self.__content.find(OVERLINE) + len(OVERLINE)]

        entry = {}

        # find description
        find_desc_end = entry_content.find("\n\n")
        entry = {"desc":entry_content[:find_desc_end].strip(":").replace("TEST ", "")}
        entry_content = entry_content[find_desc_end + len("\n\n"):]

        # find first_log
        log_raw = entry_content[entry_content.find(get_current_year()):].split("\n")[0].split(" - ")
        if len(log_raw) > 2:
            entry["first_log"] = [log_raw[1], log_raw[2]]

        entry_content = entry_content[find_desc_end:]
        begin_pass = entry_content.find(PASS_LINE)
        if begin_pass != -1 and begin_pass < entry_content.find(OVERLINE):
            entry["result"] = entry_content[begin_pass + len(PASS_LINE):].split("\n")[0]
        return entry

    def validate(self, exp_desc, exp_log=[], exp_res="PASS"):
        e = self.__entries[self.__entry_p]
        assert exp_desc == e["desc"]
        if exp_log:
            assert exp_log[0] == e["first_log"][0]
            assert exp_log[1].startswith(exp_log[1])
        if not e["desc"].startswith("Suite"):
            assert exp_res == e["result"]
        self.__entry_p = self.__entry_p + 1
