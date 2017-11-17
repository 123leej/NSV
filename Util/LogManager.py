import time
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
        result_file_name = datetime.datetime.now().strftime('%Y-%m-%d') + "_simulation.txt"
        with open("./log/" + result_file_name, "w") as result_file:
            for i in range(0, len(self.log_file)):
                with open("./log/" + self.log_file[i], "r") as node_log_file:
                    while True:
                        temp = node_log_file.readline()
                        if not temp:
                            result_file.write('\n')
                        result_file.write(temp)

        self.log_parser(result_file_name)

    def log_parser(self, _result):
        log_buffer = []
        with open("./log/" + _result, "r") as result_file:
            while True:
                temp = result_file.readline()
                if not temp:
                    break
                log_buffer.append(temp)

        log_buffer = self.parsing(log_buffer)

        with open("./log/" + _result, "w") as result_file:
            for log in log_buffer:
                result_file.write(log)

    def parsing(self, _log_buffer):
        return sorted(_log_buffer, key=self.time_to_stamp)

    def time_to_stamp(self, _log):
        temp = _log.split("|")[0]
        stamp = time.mktime(datetime.datetime.strptime(temp, "%H:%M:%S").timetuple())
        return stamp
