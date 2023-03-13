import argparse

class CommandLineParser:
    def __init__(self):
        self.__cmd_options = ["no", "h", "p", "o"]
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument('-no','--no-suite-setup', help='No Suite Prepare and Teardown', action="store_true")
        self.__parser.add_argument('-p','--json-system-params', help='Path to JSON params file.', default="system_params.json")
        self.__parser.add_argument('-o','--report-output', help='Path to report html file.', default="index.html")
        self.__custom_cmds = []

    def __cmd_opt_duplicates(self, cmd_opt):
        for c in self.__cmd_options:
            if cmd_opt == c:
                return True
        return False

    def __add_cmd_option(self, desc):
        for cmd_len in range(len(desc)):
            cmd_opt = desc[0:cmd_len + 1].lower()
            if not self.__cmd_opt_duplicates(cmd_opt):
                self.__cmd_options.append(cmd_opt)
                return cmd_opt

        raise Exception(desc + " has duplicate description")

    @staticmethod
    def desc_to_cmd(desc):
        return desc.replace(" ", "_").replace("-","_").lower()

    def add_testcase_as_cmd_option(self, desc):
        desc_cmd = CommandLineParser.desc_to_cmd(desc)
        self.__parser.add_argument('-' + self.__add_cmd_option(desc),'--' + desc_cmd, help='Test ' + desc, action="store_true")

    def parse_args(self):
        self.__args = self.__parser.parse_args()
        no_suite_setup = vars(self.__args)["no_suite_setup"]
        params_env = vars(self.__args)["json_system_params"]
        report_file = vars(self.__args)["report_output"]
        custom_env ={}
        for k in self.__custom_cmds:
            custom_env[k] = vars(self.__args)[k]
        return [no_suite_setup, params_env, report_file, custom_env]

    def cmd_arg_was_set(self, desc):
        return vars(self.__args)[CommandLineParser.desc_to_cmd(desc)]

    def add_custom_cmd_option(self, attr, desc, default=None, required=False):
        cmd = CommandLineParser.desc_to_cmd(attr)
        self.__parser.add_argument('-' + self.__add_cmd_option(cmd), '--' + cmd, help=desc, default=default, required=required)
        self.__custom_cmds.append(cmd)
