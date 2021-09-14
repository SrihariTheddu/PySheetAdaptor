
# *** Import all the required modules here...
import gspread
from PySheetAdaptor.Drivers.PySheetDriver import PySheetDriver
from PySheetAdaptor.Drivers.GoogleDriver import GoogleDriver
from sys import stdout
from PySheetAdaptor.Drivers.UtilityDriver import (
                                        BuildError,
                                        AuthenticationException,
                                        UploadError,
                                        SheetNotFoundException
                                        )
import os
#======================================================================================================================
class PySheetAdaptor(GoogleDriver, PySheetDriver):
    """
    This module PySheetAdaptor helps in interacting with the GoogleSheets API..
    To access spreadsheets via Google Sheets API you need to authenticate and authorize your application.
    Older versions of gspread have used oauth2client. Google has deprecated it in favor of google-auth.
    If you’re still using oauth2client credentials, the library will convert these to google-auth for you,
    but you can change your code to use the new credentials to make sure nothing breaks in the future.
    When you run this code, it launches a browser asking you for authentication.
    Follow the instruction on the web page. Once finished, gspread stores authorized credentials in the
    config directory next to credentials.json.
    You only need to do authorization in the browser once, following runs will reuse stored credentials.
    params:kwargs ::
        AUTO_LOGIN :: DICT (username:username, password: password)
        name :: Human Readable Name...
    """
    def __init__(self, **kwargs: object) -> None:
        # If you are running first time on the machine do not give any params..
        # It will setup the environment and make all the required configurations..
        # you need to mention your google sheet api credentials file as the path
        # whenever it asks for the credentials..
        # *** Settings Related variables...
        self.BOUNDED_ENVIRON: bool = False
        self.SERVER_SHEET: bool = False
        ## if you have already setup on local Machine you can use parametised constructor
        ## only if you want to automate the process
        ## You can skip the auto login process if you need....
        self.auto_login: bool = kwargs.pop("AUTO_LOGIN", False)
        self.error_message: str = None
        super(PySheetDriver, self).__init__()
        # Setup the Environment............
        # ie at the end of the code snippet you working directory has below struct
        # after executing above statement locally you will have created a local
        # directory with following files......
        # Dir :- guser\Credentials\user_credentials.json
        # here we have login panel which authenticates the user...
        if not self.configure_environment():
            raise EnvironmentError(f"""
            ---------------------------------------------------------------------
            couldn't build the environment...
            This is may be because invalid/not correctly patterned credentials..
            This could be due to unsuccessful login...
            Delete all the files try again..
            helpdesk :: pysheetadaptor@gmail.com
            ------------------------------------------------------------------
            """)
        stdout.write(f"""
                Environment Launched successfully({self.BASE_DIR})\n
                Building the environment with tools...
        """)
        # *** connecting with the user........
        # it setup the report handlers and accessing the user credentials...
        # it setups the MainDriver .........................
        if not self.install_driver(name=kwargs.pop("name", "pysheet")):
            raise BuildError(f"""
            couldn't build the environment...
            This may be due to error in installing handlers...
            Failed to install Main Driver...
            """)
        self.report.debug(f"""
            Successfully Installed MainDriver....
            Successfully Added Handlers....
            """)
        # *** authenticating the client.......
        # *** Authenticates the user with the provided google spreadsheet api..
        # *** installs the client to interact with spreadsheet......
        if not self.client_setup(credentials_path=self.credentials_path):
            raise AuthenticationException(f"""
            Invalid GoogleSheet API Credentials....
            Credentials url :: {self.credentials_path}
            """)
        self.success.warning(f"""
            Setup successful.......
            *****  Your workspace is ready *****
            Enjoy the day.........
            """)



    def upload_to_server(self, *args, **kwargs) -> bool:
        """
        uploads the last committed data to the sheet..
        params : None
        Here we have API Error
        To Resolve this error we need to update our sheets in batches...
        """
        try:
            # ** reload the record (to verify that data is not missed)
            # ** it updates all the status of the list....
            self.reload(*args, **kwargs)
            # ** Before updating in batches it clears the sheet...
            # # *** Now the sheet is empty.......
            self.sheet_clear(*args, **kwargs)
            self.add_back_up()
            self.current_worksheet.update(self.records)
            self.success.warning(f"Successfully uploaded to the Server url  : {self.source_url}")
            self.is_dumped = True
            return True
        except gspread.exceptions.APIError as e:
            raise UploadError(f"""
                 Couldn't upload the data to the server..
                 {e}
            """)
        except Exception as e:
            raise BaseException(f"Something went wrong.........\n{e}")

    def create_spreadsheet(self,spreadsheet_name : str, *args, **kwargs) -> bool:
        if not super().create_spreadsheet(spreadsheet_name=spreadsheet_name):
            raise SheetNotFoundException(
                f"Could not create Spreadsheet with spreadsheetname :: {spreadsheet_name}"
            )
        return True

    def open_spreadsheet(self, **kwargs) -> bool:
        if not super().open_spreadsheet(
                title = kwargs.pop("title",None),
                url=kwargs.pop("url",None),
                key=kwargs.pop("key",None)
        ):
            raise SheetNotFoundException("no sheet found")
        self.SERVER_SHEET = True
        return True

    def create_worksheet(self, worksheet_name : str = None, rows:int = 100, cols : int = 100) -> bool:
        if super().create_worksheet(
                worksheet_name=worksheet_name, rows=rows, cols=cols):
            self.install(self)
            return True
        return False

    def open_worksheet(self, title: str = None, index:int = None, *args, **kwargs) -> bool:
        self.logbook_name = kwargs.pop("logbook_name", "logbook.txt")
        self.db_restore_name = kwargs.pop("db_restore_name", "db_restore.txt")
        if super().open_worksheet(title=title, index=index):
            self.install(self)
            self.setup_record_handler()
            self.setup_backup_handler()
            self.load_from_server()
            if self.no_of_rows == 0:
                self.report.debug(
                    "*************** Worksheet Empty ***************** ")
        else:
            raise SheetNotFoundException(f"No Worksheet Found with title :: {title}")

    def set_columns(self, columns:list):
        return super().set_attributes(columns)

    @property
    def get_columns(self, columns:list) ->list:
        return self.columns

    def sheet_clear(self, *args, **kwargs):
        self.report.debug(f"clearing the worksheet.............")
        self.current_worksheet.clear()

    def close_connection(self, *args, **kwargs):
        self.report.debug("clearing sessions please wait..........")
        self.clear_environ()
        self.report.debug(" closing connection......")
        self = None
    
    @property   
    def terms_and_conditions(self) ->str:
        return f"""
             Admin Name   : {self.admin_name}
             Directory    : {os.getcwd()}
             
             This process has undertaken under the google guidelines and privacy policy of an individual user
             This data is collected from your google cloud platform with the accessibity procedure
             This software is allowed to view ,overwrite and change the data from the google cloud account...
             google Account : {self.email_id}
               ...............
             """


