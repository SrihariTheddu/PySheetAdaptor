import os
from sys import stdout, stderr
from getpass import getpass
from PySheetAdaptor.src.ResourceManager.utils import run_with_protected_environ
from PySheetAdaptor.src.exceptions import BuildError, AuthenticationError

class SystemAdmin:
    """
    It configures all the required setup and work with local mcahine....
    It setups the run time environment for the modules to work on sheets....
    It has local api to insert google apis.........
    """
    adaptor: None
    is_authorised: bool
    DIRS: list = [r"\LogBooks", r"\Storage", r"\Credentials"]

    def build(self) -> None:
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
        self.terms_and_conditions: str = f"""
             Admin Name   : {self.admin_name}
             Directory    : {os.getcwd()}
             
             This process has undertaken under the google guidelines and privacy policy of an individual user
             This data is collected from your google cloud platform with the accessibity procedure
             This software is allowed to view ,overwrite and change the data from the google cloud account...
             google Account : {self.email_id}
               ...............
             """

    #@run_with_protected_environ
    def configure_environment(self) -> None:
        # *** Configures the RunTime Environment .........
        self.build()
        self.set_environment()
    
    #@run_with_protected_environ
    def set_environment(self) -> None:
        if os.path.exists("PySheetAdaptor"):
            stdout.write("Requirement Already Satisfied...Building...\n")
        else:
            raise BuildError(f"PySheetAdaptor not installed with dir {os.getcwd()}")
            sys.exit(100)

            ## Do Something to satisy Requirements.........
        if not os.path.exists(self.user_credentials_path):
            stderr.write("There are no user credentials ............\n")
            stderr.write("Enter Credentials............\n")
            self.get_admin_details()
            self.create_admin_credentials()
        stdout.write(f"{self.BASE_DIR}\login_panel&&123456&& \n")
        self.login_panel()

    def get_admin_details(self):
        
        def validate_password() -> str:
            password,confirm_password = "","123"
            while password != confirm_password:
                stdout.write("Enter Admin Password  :  ")
                password: str = getpass()
                stdout.write("Confirm Password  :  ")
                confirm_password: str = getpass()
                stderr.write("Password mismatch..\n")
            return "quit"
        
        def validate_mail() -> str:
            while True:
                email: str = input("Enter Email Address  :  ")
                if len(email.split("."))>1 and len(email.split("@"))>1:
                    return email
                stderr.write("Invalid Mail Address..\n")
            
        self.admin_name: str = input(" Enter Admin Name  : ")
        self.admin_password: str = validate_password()
        self.email_id: str= validate_mail()
        stdout.write(" Enter Email Password : ")
        self.email_password = getpass()
        self.credentials_path = input("Enter credentials path :: ")
        while not self.agree:
            print(self.terms_and_conditions)
            print("****************" * 3)
            if input(" Enter 'AGREE' to proceed    :: ").upper() == "AGREE" :
                self.agree = True
        self.documentation()
                
    @run_with_protected_environ           
    def create_admin_credentials(self) :
        ## *** Creates the credentials for admin........
        self.credentials = f'''admin_username:{self.admin_name},admin_password:{self.admin_password},email_id: {self.email_id},email_password:{self.email_password},"credentials_path":{self.credentials_path}'''
        try:
            os.mkdir(os.getcwd() + "\guser")
        except Exception as e:
            stderr.write(f"{e}\n")
        with open(self.user_credentials_path, "w") as admin :
                admin.write(str(self.credentials))
        stdout.write(f"created credentials successfully..............\n")
    
    #@run_with_protected_environ
    def login_panel(self):

        if not os.path.isfile(self.credentials_path):
            raise AuthenticationError("No url exists setup Failed")

        with open(self.credentials_path) as admin:
            creds = admin.read()
        self.credentials = {}
        try :
            for spc in creds.split(",") :
                key, value = spc.split(":")
                self.credentials[str(key)] = str(value)
        except:
            raise AuthenticationError("Invalid format of credentials")
            
        while not self.is_authorised:
            username = input("Enter Username   ::   ")
            password = getpass()

            if self.credentials["admin_username"] == username and self.credentials["admin_password"] == password:
                self.admin_name = self.credentials["admin_username"]
                self.email_id = self.credentials["email_id"]
                self.is_authorised = True
                stdout.write("Successfully Logged in......\n")
                stdout.write(f"{self.credentials_path}\\login\\username={username}&&email={self.credentials['email_id']}\n")
                return True
            else:
                stderr.write("Incorrect username (or) password [Quit:Q]")
                if input("Enter Q to Quit  :   ").lower() == "q":
                    return False

    def install(self , adapter):
        """
          Add your file paths variables here and it will be automatically configured..
          It can be inherited from the bases and parent classes....
        """
        self.adaptor = adapter
        self.BASE_DIR = os.getcwd( )
        self.SHEET_DIR = os.path.join(self.BASE_DIR , self.adaptor.current_spreadsheet.title)
        self.logbookpath_url = os.path.join(self.SHEET_DIR + "\LogBooks", self.adaptor.current_worksheet.title + "-logbook.txt")
        self.db_restorepath_url = os.path.join(self.SHEET_DIR + "\Storage", self.adaptor.current_worksheet.title + "-db_restore.txt")
        self.admin_credentials_url = os.path.join(self.SHEET_DIR + "\Credentials" , "admin_credentials.json")
        self.base_html = os.getcwd() + r"\PySheetAdaptor\Files\base.html"
        self.files = [self.logbookpath_url , self.db_restorepath_url , self.admin_credentials_url]
        ## *** checks whether the given sheet has folder..........
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
        for dirs in self.DIRS :
            try:
                os.mkdir(self.SHEET_DIR + dirs)
                self.adaptor.report.info(f" DIR :: {self.SHEET_DIR + dirs} created successfully!!!! ")
            except Exception as e :
                self.adaptor.report.info(f"OOPs! could not create DIR :: {self.SHEET_DIR + dirs} due to {e} ")

    def install_files(self) :
        self.adaptor.report.debug("please wait...... ")
        for file in self.files:
            try:
                with open(file, "w") as f:
                    f.write("Success")
                self.adaptor.report.debug(f"configuring the file the url :: {file}")
            except Exception as e:
                self.adaptor.report.debug(f"couldn't configure the file : {file} due to {e}")

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
