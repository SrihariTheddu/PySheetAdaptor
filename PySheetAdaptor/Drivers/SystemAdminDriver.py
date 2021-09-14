import os
from sys import stdout, stderr
from getpass import getpass
from PySheetAdaptor import PySheetAdaptor
from PySheetAdaptor.Drivers.UtilityDriver import run_with_protected_environ, BuildError, InvalidCredentialsException, AuthenticationException
import logging as log

class SystemAdminDriver:
    """
    It configures all the required setup and work with local mcahine....
    It setups the run time environment for the modules to work on sheets....
    It has local api to insert google apis.........
    """

    DIRS: list = [r"\Credentials"]
    def __init__(self, **kwargs):
        # Directory Related Variables......
        self.BASE_DIR: os.path = os.getcwd()
        self.SPREAD_SHEET_DIR: os.path = ""
        self.WORKSHEET_SHEET_DIR: os.path = ""
        self.files: list = list()
        self.sheet_dirs: list = []
        # Credential related variables.....
        self.user_credentials_path: os.path = os.getcwd() + r"\guser\UserCredentials.json"
        self.credentials_path: os.path = ""
        self.credentials: dict = dict()
        self.admin_credentials_url: str = ""
        self.admin_name: str = ""
        self.admin_password: str = ""
        self.email_id: str = ""
        self.email_password: str = ""
        self.agree: bool = False
        self.is_authorised: bool = False
        # ***** Handlers Related Variables..........
        self.REPORT_LEVEL: int = kwargs.pop("REPORT_LEVEL", 10)
        self.report: log.Logger = None
        self.consoleHandler: log.StreamHandler = None
        self.consoleFormatter: log.Formatter = log.Formatter
        # *** Success Handler...
        self.success: log.Logger = None
        self.success_consoleHandler: log.StreamHandler = None
        self.success_consoleFormatter: log.Formatter = log.Formatter
        # *** Error Handler.........
        self.error: log.Logger = None
        self.error_consoleHandler: log.StreamHandler = None
        self.error_consoleFormatter: log.Formatter = log.Formatter
        # *** Record Handler...
        self.RECORD_LEVEL: int = 10
        self.logbookpath_url: str = ""
        self.logbook_name = None
        self.record: log.Logger = None
        self.LogFileHandler: log.FileHandler = None
        self.LogFileFormatter: log.Formatter = None
        # *** Backup Handler....
        self.db_restorepath_url: str = ""
        self.db_restore_name = None
        self.db_restore: log.Logger = None
        self.BackupFileHandler: log.FileHandler = None
        self.BackupFileFormatter: log.Formatter = None
        self.base_html = "guser\home.html"

    def configure_environment(self) -> bool:
        if os.path.exists("PySheetAdaptor"):
            stdout.write("Requirement Already Satisfied...Building...\n")
        else:
            return False
        if not os.path.exists(self.user_credentials_path):
            stderr.write("""
            There are no user credentials ............\n
            Creating the user credentials........
            """)
            self.get_admin_details()
            self.create_admin_credentials()
        stdout.write(f"{self.BASE_DIR}\login_panel&&123456&& \n")
        return self.login_panel()

    def get_admin_details(self):
        
        def validate_password() -> str:
            stdout.write(r"your text should not contain comma(,) and semicolon(:) \n")
            password: str = getpass()
            confirm_password: str = getpass()
            while password != confirm_password:
                stdout.write(r"your text should not contain comma(,) and semicolon(:) \n")
                password: str = getpass()
                stdout.write(r"Confirm password........\n")
                confirm_password: str = getpass()
                stderr.write("Password mismatch..\n")
            return password
        
        def validate_mail() -> str:
            while True:
                stdout.write(r"your text should not contain comma(,) and semicolon(:) \n")
                email: str = input("Enter Email Address  :  ")
                if len(email.split("."))>1 and len(email.split("@"))>1:
                    return email
                stderr.write("Invalid Mail Address..\n")

        stdout.write(r"your text should not contain comma(,) and semicolon(:) \n")
        self.admin_name: str = input(" Enter Admin Name  : ")
        self.admin_password: str = validate_password()
        self.email_id: str= validate_mail()
        stdout.write(" Enter Email Password : ")
        stdout.write(r"your text should not contain comma(,) and semicolon(:) \n")
        self.email_password = getpass()
        while not os.path.isfile(self.credentials_path):
            stdout.write(f"No File Found on path :: {self.credentials_path}")
            self.credentials_path = input("Enter credentials path :: ")

        while not self.agree:
            print(self.terms_and_conditions)
            print("****************" * 3)
            if input(" Enter 'AGREE' to proceed    :: ").upper() == "AGREE" :
                self.agree = True
        self.documentation()
                
    @run_with_protected_environ           
    def create_admin_credentials(self) :
        self.credentials = f'''admin_username>{self.admin_name},admin_password>{self.admin_password},email_id>{self.email_id},email_password>{self.email_password},credentials_path>{self.credentials_path}'''
        try:
            os.mkdir(os.getcwd() + "\guser")
        except Exception as e:
            stderr.write(f"{e}\n")
        with open(self.user_credentials_path, "w") as admin :
                admin.write(str(self.credentials))
        with open(self.base_html, "w") as admin :
                admin.write("")
        stdout.write(f"created credentials successfully..............\n")

    def login_panel(self):

        with open(self.user_credentials_path) as admin:
            creds = admin.read()
        self.credentials = {}
        try :
            for spc in creds.split(",") :
                key, value = spc.split(">")
                self.credentials[str(key)] = str(value)
        except:
            raise InvalidCredentialsException("Invalid format of credentials")

        self.credentials_path = self.credentials["credentials_path"]

        if self.auto_login!=False:
            if self.auto_login["username"] == self.credentials["admin_username"]:
                if self.auto_login["password"] == self.credentials["admin_password"]:
                    self.is_authorised = True
                    return True
            raise AuthenticationException("Incorrect Credentials")


        while not self.is_authorised:
            username = input("Enter Username   ::   ")
            password = getpass()

            if self.credentials["admin_username"] == username and self.credentials["admin_password"] == password:
                self.admin_name = self.credentials["admin_username"]
                self.email_id = self.credentials["email_id"]
                self.is_authorised = True
                stdout.write("Successfully Logged in......\n")
                stdout.write(f"{self.credentials_path}\\login\\username={username}&&email={self.credentials['email_id']}\n")
                self.credentials_path = self.credentials["credentials_path"]
                return True
            else:
                stderr.write("Incorrect username (or) password [Quit:Q]")
                if input("Enter Q to Quit  :   ").lower() == "q":
                    return False

    def install(self , adapter):
        self.BASE_DIR = os.getcwd()
        self.SPREAD_SHEET_DIR = os.path.join(self.BASE_DIR , self.current_spreadsheet.title)
        self.WORK_SHEET_DIR = os.path.join(self.SPREAD_SHEET_DIR, self.current_worksheet.title)
        self.sheet_dirs = [self.SPREAD_SHEET_DIR, self.WORK_SHEET_DIR, self.WORK_SHEET_DIR + r"\LogBooks", self.WORK_SHEET_DIR + r"\Storage" ]
        self.check_dirs()
        self.logbookpath_url = os.path.join(self.WORK_SHEET_DIR, "LogBooks\\" + self.logbook_name)
        self.db_restorepath_url = os.path.join(self.WORK_SHEET_DIR, r"Storage\\" + self.db_restore_name)
        self.admin_credentials_url = os.path.join(self.SPREAD_SHEET_DIR + r"\Credentials\\" , "admin_credentials.json")
        self.files = [self.logbookpath_url , self.db_restorepath_url ]
        self.check_files()
        self.check_setup()
    
    @run_with_protected_environ
    def check_setup(self) :
        ## *** if directory does not exists...
        if not os.path.isdir(self.SHEET_DIR):
            os.mkdir(self.SHEET_DIR)
            self.install_folders()
            self.install_files()

    @run_with_protected_environ
    def install_folders(self) :
        for dirs in self.sheet_dirs :
            try:
                os.mkdir(self.SPREAD_SHEET_DIR + dirs)
                self.report.info(f" DIR :: {self.SHEET_DIR + dirs} created successfully!!!! ")
            except Exception as e :
                self.report.info(f"OOPs! could not create DIR :: {self.SHEET_DIR + dirs} due to {e} ")

    def install_files(self) :
        self.adaptor.report.debug("please wait...... ")
        for file in self.files:
            try:
                with open(file, "w") as f:
                    f.write("Success")
                self.report.debug(f"configuring the file the url :: {file}")
            except Exception as e:
                self.report.debug(f"couldn't configure the file : {file} due to {e}")

    def check_files(self):
        for file in self.files:
            if not os.path.isfile(file):
                with open(file,"w") as f:
                    f.write("")

    def check_dirs(self):
        for dir in self.sheet_dirs:
            if not os.path.isdir(dir):
                os.mkdir(dir)

    def setup_handlers(self, *args, **kwargs):
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
        self.LogFileHandler = log.FileHandler(filename = self.logbookpath_url)
        self.LogFileHandler.setLevel(log.DEBUG)
        self.LogFileFormatter = log.Formatter(f"#Timestamp :  %(asctime)s \n %(message)s \n{'-'*200}",datefmt='%d-%m-%Y  %H:%M')
        self.LogFileHandler.setFormatter(self.LogFileFormatter)
        self.record = log.getLogger('record')
        self.record.setLevel(log.DEBUG)
        self.record.addHandler(self.LogFileHandler)
        self.report.debug(f"file handler setup successfull path :: {self.logbookpath_url}")

    def set_console_handler(self):
        self.consoleHandler = log.StreamHandler()
        self.consoleHandler.setLevel(self.REPORT_LEVEL)
        self.consoleFormatter = log.Formatter(f"\033[0;37;8m {self.command_prompt} : %(message)s \033[0;37;8m" ,datefmt='%Y-%m-%d => %H:%M ')
        self.consoleHandler.setFormatter(self.consoleFormatter)
        self.report.addHandler(self.consoleHandler)

    def set_error_console_handler(self):
        self.error_consoleHandler = log.StreamHandler()
        self.error_consoleHandler.setLevel(log.ERROR)
        self.error_consoleFormatter = log.Formatter(f"\033[0;31;8m {self.command_prompt} : %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.error_consoleHandler.setFormatter(self.error_consoleFormatter)
        self.error.addHandler(self.error_consoleHandler)

    def set_success_console_handler(self):
        self.success_consoleHandler = log.StreamHandler()
        self.success_consoleHandler.setLevel(log.WARNING)
        self.success_consoleFormatter = log.Formatter(f"\033[0;32;8m {self.command_prompt} : %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.success_consoleHandler.setFormatter(self.success_consoleFormatter)
        self.success.addHandler(self.success_consoleHandler)

    def setup_backup_handler(self, **kwargs):
        self.BackupFileHandler = log.FileHandler(filename = self.db_restorepath_url)
        self.BackupFileHandler.setLevel(log.DEBUG)
        self.BackupFileFormatter = log.Formatter(f"%(message)s",datefmt='%d-%m-%Y  %H:%M')
        self.BackupFileHandler.setFormatter(self.BackupFileFormatter)
        self.db_restore = log.getLogger('Restore')
        self.db_restore.setLevel(log.DEBUG)
        self.db_restore.addHandler(self.BackupFileHandler)

    def restore(self, **kwargs):
        for cursor in self.messages[self.bp_cursor]:
            self.back_up_data.append(cursor[1])

    def remove(self):
        for cursor in self.messages[self.bp_cursor]:
            self.back_up_data.remove(cursor[1])

    def add_back_up(self):
        for line in self.back_up_data:
            self.db_restore.debug(line)

    def clear_db(self):
        with open(self.db_restorepath_url,"w") as f:
            f.write("")

    def documentation(self)  -> None:
        print("""
            please configure your credentials below mentioned way ::
            Workspace Environment::
             ------------------------------------------------------------
            | >  SpreadSheetName                                         |
            |           > Credentials                                    |
            |                   > ......your credentials........         |
            |           > LogBooks                                       |
            |                   > Worksheet1-log-book                    | 
            |                   > Worksheet2-log-book                    |
            |                   .....................                    | 
            |                   .....................                    |
            |                   ......................                   |
            |           > Storage                                        |
            |                   > Worksheet1-db-restore                  |
            |                   > Worksheet2-db-restore                  |
            |                   .....................                    |
            |                   .....................                    |
            |                   ......................                   |
            --------------------------------------------------------------
            """)

