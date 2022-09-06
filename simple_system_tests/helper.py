import datetime
import traceback
import os
import sys

DEFAULT_OVERLINE_COLS=60

def get_overline():
    cols = DEFAULT_OVERLINE_COLS
    try:
        cols = os.get_terminal_size().columns
    except:
        pass

    ol = ""
    for _ in range(cols):
        ol = ol + "_"
    return ol + "\n"

def get_exception(ec):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    last = len(tb_lines) - 1
    return tb_lines[last - 1] + tb_lines[last]

def get_time():
    return datetime.datetime.now().timestamp()
