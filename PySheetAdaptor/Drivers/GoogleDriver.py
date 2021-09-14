
import gspread
from oauth2client.service_account import ServiceAccountCredentials, client
import logging as log
from sys import exit
import os
from json import loads
from PySheetAdaptor.Drivers.UtilityDriver import InvalidCredentialsException


class GoogleDriver:

    scope = (
              "https://spreadsheets.google.com/feeds",
              "https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive.file",
              "https://www.googleapis.com/auth/drive"
              )

    def __init__(self):
        self.credentials: ServiceAccountCredentials = ServiceAccountCredentials
        self.command_prompt: str = "@"
        self.credentials_path: os.path = os.path
        self.username = "root"
        self.credentials_as_json: dict = dict()
        self.current_worksheet: gspread.Worksheet = gspread.Worksheet
        self.current_spreadsheet: gspread.Spreadsheet = gspread.Spreadsheet
        self.client: client = client

    def client_setup(self, **kwargs) -> None:
        self.credentials_path = kwargs.pop("credentials_path", self.credentials_path)
        self.check_internet_connection()
        return self.authenticate()

    def authenticate(self) -> None:
        self.report.debug(f"Authenticating the Credentials given file path url : " + str(self.credentials_path))
        if os.path.isfile(self.credentials_path):
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, self.scope)
        else:
            raise FileExistsError("The credentials doesn't exists")
        try:
            with open(self.credentials_path, 'r') as credentials:
                self.credentials_as_json = loads(credentials.read())
        except:
            raise InvalidCredentialsException(f"Invalid Json format :: {self.credentials_path}")

        self.command_prompt += self.credentials_as_json["project_id"].split("-")[0]+"-"+self.credentials_as_json["project_id"].split("-")[1]
        self.consoleFormatter = log.Formatter(f"\033[0;35;8m {self.command_prompt} : %(levelname)s- %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.consoleHandler.setFormatter(self.consoleFormatter)
        self.client = gspread.authorize(self.credentials)
        if self.client.auth:
            self.success.warning(f"Client Authorised Successfully.........")
            self.report.debug(f" Client Id   :: " + str(self.credentials.client_id))
            self.report.debug(f"Client Mail Id  ::  " + str(self.credentials.service_account_email))
            return True
        else:
            raise ConnectionAbortedError(f"Authentication Failed......")

    def open_spreadsheet(self, title: str = None, url: str = None, key: str = None) -> bool:
        if title:
            try:
                self.current_spreadsheet = self.client.open(title=title)
            except Exception as e :
                self.error.error(f"No SpreadSheet Found with Title "+title+"\n")
                return False
        elif url:
            try:
                self.current_spreadsheet = self.client.open_by_url(url)
            except Exception as e :
                self.error.error(f"No SpreadSheet Found with url  ::  "+url)
                return False
        elif key:
            try:
                self.current_spreadsheet = self.client.open_by_key(key)
            except Exception as e:
                self.error.error("No Sheet with KEY "+key)
                return False
        else:
            return False
        self.consoleFormatter = log.Formatter(f"\033[0;40;8m{self.command_prompt} :%(levelname)s- %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.consoleHandler.setFormatter(self.consoleFormatter)
        self.success.warning(f"Spreadsheet loaded successfully with {self.current_spreadsheet}")
        return True

    def create_spreadsheet(self,spreadsheet_name : str, *args, **kwargs) -> bool:
        if not spreadsheet_name:
            self.error.error("Mention the spreadsheet name to create")
            return False
        try:
            self.current_spreadsheet = self.client.create(spreadsheet_name)
            self.command_prompt += f"@{self.current_spreadsheet.title}"
            self.consoleFormatter = log.Formatter(f"{self.command_prompt} : %(levelname)s- %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
            self.consoleHandler.setFormatter(self.consoleFormatter)
            self.report.info("Spreadsheet created successfully.. "+str(self.current_spreadsheet.title))
            return True
        except Exception as e:
            self.error.error("Couldn't create the spreadsheet with title "+str(spreadsheet_name))
            self.error.error(e)
            return False

    def share_spreadsheet(self,spreadsheet: gspread.Spreadsheet = None, url : str = None, perm_type : str = None, role : str = None) -> bool:
        if url and perm_type and role:
            try:
                if spreadsheet :
                    spreadsheet.share(url, perm_type = perm_type, role = role)
                else:
                    self.current_spreadsheet.share(url, perm_type = perm_type, role = role)
            except Exception as e:
                self.error.error("OOPs !!! couldn't share the sheet....")
                return False
            self.report.warning("Sharing the sheet to the url " + str(url))
            return True
        self.report.info("mention the parameters to share the spreadsheet...")

    def create_worksheet(self, worksheet_name : str = None, rows:int = 100, cols : int = 100) -> bool:
        if not worksheet_name:
            return False
        try:
            self.current_worksheet = self.current_spreadsheet.add_worksheet(title = worksheet_name, rows = rows, cols = cols)
            self.report.error(" New Worksheet Created by worksheetname : "+ str(worksheet_name))
            self.command_prompt += f"@{self.current_worksheet.title}"
            self.consoleFormatter = log.Formatter(f" \033[0;40;8m {self.command_prompt} : %(levelname)s- %(message)s \033[0;30;8m" ,datefmt='%Y-%m-%d => %H:%M ')
            self.consoleHandler.setFormatter(self.consoleFormatter)
            return True
        except Exception as e:
            self.error.error("Could not create the Worksheet on the worksheet Name  :  "+worksheet_name)
            self.error.error(e)
            return False

    def open_worksheet(self, title: str = None, index:int = None) -> bool:
        if title:
            try:
                self.current_worksheet = self.current_spreadsheet.worksheet(title)
            except Exception as e :
                self.error.error("No WorkSheet with Title "+ str(title))
                return False
        elif index:
            try:
                self.current_worksheet = self.current_spreadsheet.get_worksheet(index)
            except Exception as e :
                self.error.error("No WorkSheet with URL "+ str(index))
                return False
        else:
            try:
                self.current_worksheet = self.current_spreadsheet.sheet1
            except Exception as e:
                self.error.error("No WorkSheet Found............ ")
                return False
        self.success.debug(f"Worksheet Opened Successfully with Title  :: {self.current_worksheet.title} && url = {self.current_worksheet.url}")
        self.command_prompt += f"@{self.current_worksheet.title}"
        self.consoleFormatter = log.Formatter(f"\033[0;36;8m {self.command_prompt} : %(levelname)s- %(message)s \033[0;36;8m" ,datefmt='%Y-%m-%d => %H:%M ')
        self.consoleHandler.setFormatter(self.consoleFormatter)
        return True

    def delete_worksheet(self, worksheet : gspread.Worksheet = None) -> bool:
        if (type(worksheet) != gspread.Worksheet or type(worksheet) == str) and worksheet != None:
            return False
        if worksheet:
            self.current_spreadsheet.del_worksheet(worksheet)
            self.current_worksheet = None
            self.report.warning("worksheet Deleted successfully " + str(self.current_worksheet))
            return True
        else:
            try:
                self.current_spreadsheet.del_worksheet(self.current_worksheet)
                self.current_worksheet = None
                self.record.warning("worksheet Deleted successfully " + str(self.current_worksheet))
                cmd_roots = self.command_prompt.split("@")
                self.command_prompt = "@"+str(cmd_roots[0]) + "@"+str(cmd_roots[1])
                self.consoleFormatter = log.Formatter(f" {self.command_prompt} : %(levelname)s- \033[0;31;8m%(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
                self.consoleHandler.setFormatter(self.consoleFormatter)
                return True
            except Exception as e:
                self.report.error(e)
                return False

    def check_internet_connection(self) -> None:
        import urllib.request as request
        try:
            with request.urlopen('http://google.com') as server:
                pass
        except:
            self.error.error("OOPs!!! Check Your Internet Connection.....")
            exit(100)

    @property
    def test_credentials(self):
        return r"D:\PYTHON TECHNOLOGY\PROJECTS\PySheetAdaptor Package\Credentials\CreatorCredentials.json"
    @property
    def test_spreadsheet_url(self):
        return r"https://docs.google.com/spreadsheets/d/13iG1TY1222nhtSumrO7J3hSUFloQM-qfQ4-OuH-YkVU/edit?usp=sharing"


