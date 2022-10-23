import datetime


class Logger():
    def __init__(self, path):
        self.path = path
        self.file_name = f"{self.path}/log_" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".log"

    def _write_log_to_file(self, data):
        with open(self.file_name, 'a', encoding='utf-8') as logger_file:
            logger_file.write(data)

    def add_log(self, what, flags):
        choose = ['Delete:', 'Create:', 'Update:']
        prn_data = '{}\t {:5} {}'.format(str(datetime.datetime.now().strftime("%Y-%m-%d \\ %H-%M-%S")), choose[flags], what)
        add_data = prn_data + '\n'
        self._write_log_to_file(add_data)
        print(prn_data)
