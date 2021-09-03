##             ***         PYSHEET ADAPTOR         *****
## *** AN EFFICIENT MODULE TO WORK WITH WORKSHEETS............
## @Author       :: Theddu Srihari
## @EmailID      :: sriharitheddu02@gmail.com.....
## @Date         :: 11-09-2021
## Requirements  :: pandas, numpy, matplotlib, os, sys modules........
## Supported Versions..................................................
## github link ::
#=========================================================================================================================================================
# *** Import all the required modules here...

from PySheetAdaptor.src.Manager.PySheetManager import PySheetManager
from PySheetAdaptor.src.client.GoogleClient import GoogleClient
from sys import stdout, stderr
from PySheetAdaptor.src.ResourceManager.utils import run_with_protected_environ


#=========================================================================================================================================================

class PySheetAdaptor(GoogleClient, PySheetManager):

    ## *** checks the requirements satisfied.............
    #@run_with_protected_environ
    def __init__(self):
        ## *** set up the Runtime Environment
        self.REPORT_LEVEL = 10
        self.RECORD_LEVEL = 20
        self.BOUNDED_ENVIRON = True
        self.error_message = ""
        self.credentials_url = None
        try:
            self.configure_environment()
            stdout.write(f"Environment Launched successfully({self.BASE_DIR})\n")
        except Exception as e:
            stderr.write(f"oops!!! couldn't setup Environment")
            stderr.write(f"{e}\n")


    def connect(self, credentials_url=None):
        if credentials_url is not None:
            self.credentials_path = credentials_url
        # *** Setting all the requirements..........
        self.adaptor_setup(name="google_client")
        self.report.debug("loading client details .................")
        self.client_setup(credentials_url=self.credentials_path)
        self.success.warning("Setup successfully.......")


    def load_from_server(self):
        self.source_url = str(self.current_worksheet.url)
        self.source_name = str(self.current_worksheet.title)
        self._load_()
        self._map_()
        self.is_dumped = False

    @run_with_protected_environ
    def upload_to_server(self):
        try:
            self.reload()
            self.sheet_clear()
            self.current_worksheet.update(self.records)
            self.success.warning(f"Successfully uploaded to the Server url  : {self.source_url}")
            self.is_dumped = True
        except Exception as e:
            self.error.error(f"OOps!!! could n't upload ... due to {e}")
            self.error.error("Your data may have corrupted........")

    @run_with_protected_environ
    def create_spreadsheet(self,spreadsheet_name : str = None) -> bool:
        return super().create_spreadsheet(spreadsheet_name=spreadsheet_name)

    #@run_with_status_bar
    def open_spreadsheet(self, **kwargs) -> bool:
        return super().open_spreadsheet(title = kwargs.pop("title",None), url=kwargs.pop("url",None), key=kwargs.pop("key",None))

    def create_worksheet(self, worksheet_name : str = None, rows:int = 100, cols : int = 100) -> bool:
        super().create_worksheet(worksheet_name=worksheet_name, rows=rows, cols=cols)
        self.install(self)

    def open_worksheet(self, title: str = None, index:int = None) -> bool:
        super().open_worksheet(title=title, index=index)
        self.install(self)
        self.setup_record_handler()
        self.setup_backup()
        self.load_from_server()
        if self.no_of_rows == 0:
            self.report.debug("*************** Worksheet Empty ***************** ")

    def set_columns(self, columns:list):
        return super().set_attributes(columns)

    @property
    def get_columns(self, columns:list):
        return self.columns

    def sheet_clear(self):
        self.report.debug(f"clearing the worksheet.............")
        self.current_worksheet.clear()


    def print_sheet(self):
        stdout.write(self.dataframe)
        stdout.write(f"\n To update the data please update the sheet.........")

    def close_connection(self):
        self.report.debug("clearing sessions please wait..........")
        self.clear_environ()
        self.report.debug(" closing connection......")
        self = None

    def set_path(self, *args, **kwargs):
        path = None
        if len(args)>1:
            path = args[1]
        else:
            path = kwargs.pop("path",None)
        if path is not None:
            self.credentials_url = path
            self.credentials_path = path
            self.report.debug("path setup successfull.............")






