import os
import logging as log
import pandas as pd
import re
import csv
from PySheetAdaptor.Drivers.UtilityDriver import DestinationEngineNotAvailableException
## ====================================================================================================================

class BackupDriver:
    """
    Backups the data from the backup file.......
    Backup is the process of creating a copy of the data on your system that you use for recovery in case your original
    data is lost or corrupted.You can also use backup to recover copies of older files if you have deleted them from
    your system....
    """
    def __init__(self,  *args, **kwargs) -> None:
        self.files = kwargs.pop("files", [])
        self.file_name = kwargs.pop("file_name", None)
        self.records = [[],]*int(kwargs.pop("size",2000))
        self.data = ""
        self.dataframe = pd.DataFrame
        self.count = 0
        self.indexes = [None]*int(kwargs.pop("size",2000))
        self.record_lines = []
        self.backed_up_data: str = ""
        self.data_size: int = 0
        self.report: log.Logger = None
        self.consoleFormatter: log.Formatter = None
        self.consoleHandler: log.StreamHandler = None
        self.data_batch_with_dates: dict = dict()
        self.total_transactions = 0
        self.destination_url = None
        self.destination_name = None
        self.set_status_handlers()

    def set_status_handlers(self, *args, **kwargs) -> None:
        self.report = log.getLogger('Report')
        self.report.setLevel(log.DEBUG)
        self.consoleHandler = log.StreamHandler()
        self.consoleHandler.setLevel(log.DEBUG)
        self.consoleFormatter = log.Formatter(f"%(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.consoleHandler.setFormatter(self.consoleFormatter)
        self.report.addHandler(self.consoleHandler)

    def config_data_from_files(self) -> bool:
        if len(self.files)>0:
            for file in self.files:
                if os.path.isfile(file):
                    with open(file, "r") as data:
                        file_data = data.readlines()
                    self.data += file_data
                    self.report.info(f"Data collected from the file :: {file}")
                else:
                    self.report.error(f"""
                    OOPs!!!! NoFilesFound.........
                    couldn't read the data......
                    """)
                    raise FileNotFoundError(f"No file exists with file url :: {file}")
        else:
            if os.path.isfile(self.file_name):
                with open(self.file_name, "r") as data:
                    self.data = data.readlines()
                self.report.info(f"Data collected from the file :: {self.file_name}")
            else:
                self.report.error(f"""
                    OOPs!!!! NoFileFound.........
                    couldn't read the data......
                    """)
                raise FileNotFoundError(f"No file exists with file url :: {self.file_name}")


    def parse_as_logbook(self):
        lines = []
        self.report.info(f"Parsing data as logbook parser....")
        for line in self.data:
            lines.append(line)
            if line[0] == "-":
                self.record_lines.append(lines)
                self.total_transactions += 1
                lines = []
        self.report.info(f"""
            Data parsed successfully....
            file url                 :: {self.file_name}
            Total no of Transactions :: {self.total_transactions}
            """
                         )

    def get_all_logs(self, key):
        if key is None or key == "":
            return [[None, None, None]]
        logs = []
        self.report.info(f"Getting all logs with key = {key}")
        for lines in self.record_lines:
            pattern = re.compile(key)
            matches = pattern.finditer(lines[1])
            for match in matches:
                logs.append(lines)
                break
        return logs

    def print_logs(self, logs):
        for log in logs:
            print(log[0],log[1],log[2],end=" ")

    def parse_command(self, line):
        is_row_level = False
        commands = line.split("-")
        if commands[0] == "Insert":
            record = commands[2].split(":")
            self.records[int(commands[1])] = record
            self.indexes[int(commands[1])] = record[0]
            is_row_level = True
        elif commands[0] == "Delete":
            self.records[int(commands[1])] = None
            self.indexes[int(commands[1])] = None
            is_row_level = True
        elif commands[0] == "Attributes":
             self.records[0] = commands[2].split(":")
             is_row_level = True
        elif commands[0] == "Update":
             self.records[int(commands[1])] = commands[2].split("->")[0].split(":")
             is_row_level = True
        elif commands[0] == "Add Column":
            self.records[0].append(commands[1])
            for idx in range(1,len(self.records)):
                self.records[idx].append(commands[2])
            is_row_level = False
        elif commands[0] == "Delete Column":
            cindex = self.records[0].indexOf(commands[1])
            for idx in range(len(self.records)):
                self.records[idx].remove(self.records[idx][cindex])
            is_row_level = False
        if is_row_level:
            if self.count<int(commands[1]):
                self.count = int(commands[1])

    def parse_data_as_restore(self):
        self.data = reversed(self.data)
        for line in self.data:
            try:
                self.parse_command(line)
            except Exception as e:
                self.report.error(e)
        self.dataframe = pd.DataFrame(self.records[1:self.count+1],index = self.indexes[1:self.count+1], columns = self.records[0])
        return pd.DataFrame(
            list(map(lambda y:list(y),list(filter(lambda x: None not in x,self.dataframe.values)))),
            columns = self.dataframe.columns
        )

    def dump(self, destination_url=None, destination_name=None):
        self.destination_url = destination_url
        self.destination_name = os.path.basename(self.destination_url) if destination_name is None else destination_name
        try:
            return self._dump_()
        except:
            raise DestinationEngineNotAvailableException(f"No Destination Found with url  :: {self.destination_url}")

    def _dump_(self):
        if self.destination_name[-3:] == "csv":
            try:
                self.dataframe.to_csv(self.destination_name, encoding='utf-8', index=False)
            except:
                self.manual_dump(destination_url=self.destination_url)
            finally:
                pass
            self.report.warning(f"Dumped to file successfully file url(csv): {self.destination_url}")
            return True
        elif self.destination_name[-4] == "xlsx":
            with pd.ExcelWriter(self.destination_name) as writer:
                self.dataframe.to_excel(writer)
            self.report.warning(f"Dumped to file successfully file url(excel): {self.destination_url}")
            return True
        else:
            raise DestinationEngineNotAvailableException(f"No Destination Found with url  :: {self.destination_url}")

    #@run_with_protected_environ
    def manual_dump(self, destination_url):
        with open(destination_url, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.columns)
            writer.writerows(self.records)
        self.report.warning(f"Dumped to file successfully file url(csv): {destination_url}")


























