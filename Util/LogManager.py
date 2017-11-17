import datetime
from Exception.NSVExceptions import LogFileWriteError


class LogManager:
    def __init__(self):
        self.log_file = []
        self.log_file_buffer = []

    def open_log_file(self, _node_number):
        self.log_file.append("node" + str(_node_number) + "_log.txt")
        self.log_file_buffer.append(open("./log/" + self.log_file[_node_number], "a"))

    def write_log(self, _node_number, _log):
        try:
            self.log_file_buffer[_node_number].write(_log + "\n")
        except Exception:
            raise LogFileWriteError('LogFileWriteError: "' + self.log_file[_node_number] + 'file can\'t open')

    def save_logs(self):
        for i in range(0, len(self.log_file_buffer)):
            self.log_file_buffer[i].close()

        self.log_file_buffer = None

    def merge_log_files(self):
        with open("./log/" + datetime.datetime.now().strftime('%Y-%m-%d') + "_simulation", "w") as result_file:
            for i in range(0, len(self.log_file)):
                with open("./log/" + self.log_file[i], "r") as node_log_file:
                    while True:
                        temp = node_log_file.readline()
                        if not temp:
                            result_file.write('\n')
                        result_file.write(temp)
                        # TODO PARSE log datas by timelaps

