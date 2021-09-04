
#=====================================================================================================================
from PySheetAdaptor.src.Manager.PySheetManager import PySheetManager
from PySheetAdaptor.src.client.GoogleClient import GoogleClient
from sys import stdout, stderr
from PySheetAdaptor.src.ResourceManager.utils import run_with_protected_environ
from PySheetAdaptor.src.exceptions import BuildError, AuthenticationException, UploadError, SheetNotFoundException
import os

#======================================================================================================================
class PySheetAdaptor(GoogleClient, PySheetManager):

    def __init__(self):
        self.REPORT_LEVEL: int = 10
        self.RECORD_LEVEL: int = 10
        self.BOUNDED_ENVIRON: bool = False
        self.error_message: str = ""
        self.SERVER_SHEET: bool = False
        self.adaptor = None
        self.user_credentials_path: os.path = os.getcwd() + r"\guser\UserCredentials.json"
        self.credentials_path = ""
        self.credentials: dict = dict()
        self.agree: bool = False
        self.email_password: str = ""
        self.email_id: str = ""
        self.BASE_DIR: os.path = os.getcwd()
        self.admin_password: str = ""
        self.admin_name: str = ""
        self.is_authorised: bool = False
        self.logbookpath_url: str = ""
        self.db_restorepath_url: str = ""
        self.admin_credentials_url: str = ""
        self.SHEET_DIR: str = ""
        self.files: list = list()
        self.progress_bar: bool = True
        self.terms_and_conditions: str = f"""
             Admin Name   : {self.admin_name}
             Directory    : {os.getcwd()}
             
             This process has undertaken under the google guidelines and privacy policy of an individual user
             This data is collected from your google cloud platform with the accessibity procedure
             This software is allowed to view ,overwrite and change the data from the google cloud account...
             google Account : {self.email_id}
               ...............
             """

    def setup(self, *args, **kwargs) -> boolean:
        """
        it sets the local environment for working on spreadhseet....
        It checks the python version, related packages are installed on your local system to work 
        with the pysheet adaptor..
        If Modules are not available then throws an Environmenttal setup error......
        It checks whether you have user credentials (or) already you have a setup 
        if yes :- it setup the logging system by using those credentials(like google client api credentials)
        if not :- then it collects the information if the info is valid it setups the local environment.....
        if locally inherits the PySheetResourceManager 
        """
        if not self.configure_environment():
            raise EnvironmentError("couldn't setup environment")
        stdout.write(f"Environment Launched successfully({self.BASE_DIR})\n")
        return True

    def connect(self, *args, **kwargs) -> boolean:
        """
        It takes the credentials from your local files and authorizes it with by using google api
        if invalid credentials then throws the Builderror........
        """
        if not self.adaptor_setup(name="google_client"):
            raise BuildError("couldn't build the environment...")
        self.report.debug("loading client details .................")
        if not self.client_setup(credentials_path=self.credentials_path):
            raise AuthenticationException("couldn't setup the clientup.......")
        self.success.warning("Setup successfully.......")
        return True

    def upload_to_server(self) -> boolean:
        try:
            self.reload()
            self.sheet_clear()
            self.back_up()
            self.current_worksheet.update(self.records)
            self.success.warning(f"Successfully uploaded to the Server url  : {self.source_url}")
            self.is_dumped = True
            return True
        except Exception as e:
            self.error.error(f"OOps!!! could n't upload ... due to {e}")
            self.error.error("Your data may have corrupted........")
            raise UploadError("couldn't upload.....")

    def create_spreadsheet(self,spreadsheet_name : str = None) -> bool:
        if not super().create_spreadsheet(spreadsheet_name=spreadsheet_name):
            raise SheetNotFoundException(f"Couldn't create the sheet with name {spreadsheet_name}") 
        return True

    def open_spreadsheet(self, **kwargs) -> bool:
        if not super().open_spreadsheet(title = kwargs.pop("title",None), url=kwargs.pop("url",None), key=kwargs.pop("key",None)):
            raise SheetNotFoundException("no sheet found")
        self.SERVER_SHEET = True
        return True

    def create_worksheet(self, worksheet_name : str = None, rows:int = 100, cols : int = 100) -> bool:
        if super().create_worksheet(worksheet_name=worksheet_name, rows=rows, cols=cols):
            self.install(self)
        else:
            raise SheetNotFoundException("Couldn't create the sheet")

    def open_worksheet(self, title: str = None, index:int = None) -> bool:
        if super().open_worksheet(title=title, index=index):
            self.install(self)
            self.setup_record_handler()
            self.setup_backup()
            self.load_from_server()
            if self.no_of_rows == 0:
                self.report.debug("*************** Worksheet Empty ***************** ")
        else:
            raise SheetNotFoundException(f"No Worksheet Found with title :: {title}")

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



