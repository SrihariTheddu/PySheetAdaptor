
import logging as log
from os import path

class BackupHandler:

    def __init__(self, **kwargs):
        self.FileHandler = log.FileHandler(filename = self.db_restorepath_url)
        self.FileHandler.setLevel(log.DEBUG)
        self.FileFormatter = log.Formatter(f"%(message)s",datefmt='%d-%m-%Y  %H:%M')
        self.FileHandler.setFormatter(self.FileFormatter)
        self.db_restore = log.getLogger('Restore')
        self.db_restore.setLevel(log.DEBUG)
        self.db_restore.addHandler(self.FileHandler)


    def restore(self, **kwargs):
        for cursor in self.messages[self.bp_cursor]:
            self.back_up_data.append(cursor[1])

    def back_up(self):
        for line in self.back_up_data:
            self.db_restore.debug(line)

    def clear_db(self):
        with open(self.filename,"w") as f:
            f.write("")


class MainHandler(BackupHandler):

    def __init__(self, *args, **kwargs):
        self.logbookpath_url: path
        self.consoleFormatter: log.Formatter
        self.consoleHandler: log.StreamHandler
        self.report: log.Logger
        self.record: log.Logger
        self.setup_report_handler(*args, **kwargs)
        self.success.debug(f"Report Handler setup successfully...{self.report.name}")
        self.success.debug(f"Report Handler Level  :<Level  :{self.report.getEffectiveLevel()}")

    def setup_report_handler(self, *args, **kwargs):
        self.report = log.getLogger('Report')
        self.report.setLevel(self.REPORT_LEVEL)
        self.set_console_handler()
        self.report.info("Report Handler set successfull.......")

        self.error = log.getLogger('error')
        self.set_error_console_handler()
        self.error.setLevel(log.ERROR)
        self.error.error("Error Handler set successfull......(Ignore Text color)")

        self.success = log.getLogger('success')
        self.success.setLevel(log.WARNING)
        self.set_success_console_handler()
        self.success.warning("Success Handler set successfull......(Ignore Text color)")



    def setup_record_handler(self):
        # *** creating the file logger which output into the file system
        # it is set to the DEBUG , where every level of message is directly logged on to file
         # *** For testing change it to CRITICAL
        self.record = log.getLogger('Record')
        self.record.setLevel(self.RECORD_LEVEL)
        # Now Binding the File handler...
        # ** configures the File handler
        self.set_file_handler()

    def setup_backup(self):
        super().__init__()

    def set_file_handler(self):
        # *** Adding the file to the Log Handler...
        self.FileHandler = log.FileHandler(filename=self.logbookpath_url)
        # *** setting level to the Handler
        self.FileHandler.setLevel(self.RECORD_LEVEL)
        # *** setting the formatter to the handler
        self.FileFormatter = log.Formatter(f"#Timestamp :  %(asctime)s \n %(message)s\n--------------------------------------------------------------------------------------------------------",datefmt='%d-%m-%Y  %H:%M')
        self.FileHandler.setFormatter(self.FileFormatter)
        self.record.addHandler(self.FileHandler)
        self.report.addHandler(self.FileHandler)

    def set_console_handler(self):
        # *** get the stream handler by using the logging module
        self.consoleHandler = log.StreamHandler()
        # *** setting level to the Handler
        self.consoleHandler.setLevel(self.REPORT_LEVEL)
        # *** setting the formatter to the handler
        self.consoleFormatter = log.Formatter(f"\033[0;40;8m{self.command_prompt} : %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.consoleHandler.setFormatter(self.consoleFormatter)
        self.report.addHandler(self.consoleHandler)


    def set_error_console_handler(self):
        # *** get the stream handler by using the logging module
        self.error_consoleHandler = log.StreamHandler()
        # *** setting level to the Handler
        self.error_consoleHandler.setLevel(log.ERROR)
        # *** setting the formatter to the handler
        self.error_consoleFormatter = log.Formatter(f"\033[0;31;8m{self.command_prompt} : %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.error_consoleHandler.setFormatter(self.error_consoleFormatter)
        self.error.addHandler(self.error_consoleHandler)


    def set_success_console_handler(self):
        # *** get the stream handler by using the logging module
        self.success_consoleHandler = log.StreamHandler()
        # *** setting level to the Handler
        self.success_consoleHandler.setLevel(log.WARNING)
        # *** setting the formatter to the handler
        self.success_consoleFormatter = log.Formatter(f"\033[0;32;8m {self.command_prompt} : %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.success_consoleHandler.setFormatter(self.success_consoleFormatter)
        self.success.addHandler(self.success_consoleHandler)



