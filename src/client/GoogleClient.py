
# *** to communicate through the Google spreadsheet.....
import time

import gspread
# *** Handling the service Credentials.....
from oauth2client.service_account import ServiceAccountCredentials
# *** used to handle all the log functions...
import logging as log
# *** These modules are used to handle the system calls
from sys import exit, stdout
import os
# *** Used to handle the credentials....
from json import loads
import pandas as pd
from abc import ABC

class GoogleClient(ABC):
    """
        To access spreadsheets via Google Sheets API you need to authenticate and authorize your application.
        Older versions of gspread have used oauth2client. Google has deprecated it in favor of google-auth.
        If you’re still using oauth2client credentials, the library will convert these to google-auth for you,
        but you can change your code to use the new credentials to make sure nothing breaks in the future.
        When you run this code, it launches a browser asking you for authentication.
        Follow the instruction on the web page. Once finished, gspread stores authorized credentials in the
        config directory next to credentials.json.
        You only need to do authorization in the browser once, following runs will reuse stored credentials.
        :param kwargs:
    """
    # *** an API used to manipulate data with python objects..........
    factory = None

    def client_setup(self, **kwargs ):
        self.current_spreadsheet = gspread.Spreadsheet
        self.current_worksheet = gspread.Worksheet
        self.credentials_as_json: dict = dict()
        self.username = "root"
        # *** Control all the variables....
        self.credentials = None
        self.credentials_path = kwargs.pop("credentials_url",self.credentials_path)
        # *** Text used to display as the command prompt.............
        self.command_prompt = "@"
        # *** scope of the server to access all the fields.....
        # *** Mention all the variables here...
        self.scope = (
              "https://spreadsheets.google.com/feeds",
              "https://www.googleapis.com/auth/spreadsheets",
              "https://www.googleapis.com/auth/drive.file",
              "https://www.googleapis.com/auth/drive"
              )
        # *** Mentioning the credentials path url...........
        # check the Internet connection here.....
        self.check_internet_connection()
        # *** Authenticate the user......
        self.authenticate(credentials_path = self.credentials_path)


    def check_internet_connection(self) -> None:
        """
        checks the internet connection , if has internet connection has allowed for further process
        else exits the system will the exit status 100.....
        Open your Settings app "Wireless & networks" or "Connections".
        Depending on your device, these options may be different.
        Turn Wi-Fi off and mobile data on, and check to see if there's a difference.
        turn mobile data off and Wi-Fi on and see if that works.
        :return:
        """
        import urllib.request as request
        try:
            with request.urlopen('http://google.com') as server:
                pass
        except Exception as e:
            self.error.error("OOPs!!! Check Your Internet Connection.....")
            exit(100)


    def authenticate(self, credentials:dict = None, credentials_path : os.path = None) -> None:
        """
        authenticate the user with the following credentials and creates the client object
        :param credentials:  json file format credentials....
        :param credentials_path:  file path for credentials.....
        :return: it returns npne
        """
        if credentials_path:
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, self.scope)
        elif credentials:
            self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials, self.scope)
        # *** getting the project details of the client...
        with open(self.credentials_path, 'r') as fs:
            self.credentials_as_json = loads(fs.read())
        self.command_prompt += self.credentials_as_json["project_id"].split("-")[0]+"-"+self.credentials_as_json["project_id"].split("-")[1]
        # *** setting the formatter to the handler
        # *** setting the formatter to the handler
        self.consoleFormatter = log.Formatter(f"\033[0;40;8m {self.command_prompt} : %(levelname)s- %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.consoleHandler.setFormatter(self.consoleFormatter)
        # Authorising the Client with the given credentials...
        self.report.debug(f"Authenticating the Credentials given file path url : "  + str(self.credentials_url))
        self.report.debug(f" Client Id   :: " + str(self.credentials.client_id))
        self.report.debug(f"Client Mail Id  ::  " + str(self.credentials.service_account_email))
        self.client = gspread.authorize(self.credentials)
        # Validating the Client...
        if self.client.auth:
            self.success.warning(f" Client Authorised Successfully.........")
        else:
            self.error.error(f"  OOPs!!! Invalid Authentication ")


    def load_data_from_csv(self, file_path_url : str, append:bool = False ) -> int:
        # *** load data from the csv file using python pandas module.....
        # *** Read those data as form as list...........
        try:
            dataframe = pd.read_csv(file_path_url)
            values_list = [dataframe.columns.values.tolist()] + dataframe.values.tolist()
        except Exception as e:
            return False
        # *** append the data to file........................
        if not append:
            self.current_modeladaptor.batch_update(values_as_list=values_list)
            self.report.info(f"Data Loaded successfully from the csv file name : {file_path_url}")
            return 1
        else:
            for index, values in enumerate(values_list):
                self.current_modeladaptor.insert_at(values,index)
            return 2
        return 0


    def open_spreadsheet(self, title:str = None, url:str = None, key:str = None) -> bool:
        """
        You can open a spreadsheet by its title as it appears in Google Docs:
        sh = gc.open('My poor gym results')
        If you want to be specific, use a key (which can be extracted from the spreadsheet’s url):
        sht1 = gc.open_by_key('0BmgG6nO_6dprdS1MN3d3MkdPa142WFRrdnRRUWl1UFE')
        Or, if you feel really lazy to extract that key, paste the entire spreadsheet’s url
        sht2 = gc.open_by_url('https://docs.google.com/spreadsheet/ccc?key=0Bm...FE&hl')
        :param title:
        :param url:
        :param key:
        :return:
        """
        # open the Spreadsheet by the given title of the spread sheet....
        if title:
            try:
                self.current_spreadsheet = self.client.open(title=title)
            except gspread.SpreadsheetNotFound as e :
                self.error.error(f"No SpreadSheet Found with Title "+title+"\n")
                return False
        # open the spreadsheet by the url of the given spread sheet
        elif url:
            try:
                self.current_spreadsheet = self.client.open_by_url(url)
            except gspread.SpreadsheetNotFound as e :
                self.error.error(f"No SpreadSheet Found with url  ::  "+url)
                return False
        # open the spreadsheet by the key of the given spread sheet
        elif key:
            try:
                self.current_spreadsheet = self.client.open_by_key(key)
            except gspread.SpreadsheetNotFound as e:
                self.error.error("No Sheet with KEY "+key)
                return False
        else:
            return False
        # *** if spreadsheet is opened successfully than activate all the given handlers to moniter the spread sheet..
        # *** Moniter/handlers are the super class of Current Adaptor
        #self.command_prompt += f"@{self.current_spreadsheet.title}"
        # *** setting the formatter to the handler
        self.consoleFormatter = log.Formatter(f"\033[0;40;8m{self.command_prompt} :%(levelname)s- %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.consoleHandler.setFormatter(self.consoleFormatter)
        self.success.warning(f"Spreadsheet loaded successfully with {self.current_spreadsheet}")


        # *** Log the info onto console......
        return True

    def create_spreadsheet(self,spreadsheet_name : str = None) -> bool:
        """
        Use create() to create a new blank spreadsheet:
        sh = gc.create('A new spreadsheet')
        Note: If you’re using a service account, this new spreadsheet will be visible only to this account. To be able to access
        newly created spreadsheet from Google Sheets with your own Google account you must share it with your email.
        See to share a spreadsheet in the section below.
        :param spreadsheet_name:
        :return:
        """
        #*** if title of the spreadsheet is not mentioned than throw fasle statement to create spreadsheet
        if not spreadsheet_name:
            self.error.error("Mention the spreadsheet name to create")
            return False
        #*** create the spreedsheet with the given parameters....
        try:
            self.current_spreadsheet = self.client.create(spreadsheet_name)
            # *** if spreadsheet is opened successfully than activate all the given handlers to moniter the spread sheet.
            # *** Moniter/handlers are the super class of Current Adaptor
            self.command_prompt += f"@{self.current_spreadsheet.title}"
            # *** setting the formatter to the handler
            self.consoleFormatter = log.Formatter(f"{self.command_prompt} : %(levelname)s- %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
            self.consoleHandler.setFormatter(self.consoleFormatter)
            # *** Log the info onto console and into the log file.....
            self.record.info(f"Spreadsheet Created by the {self.current_spreadsheet.title}")
            #self.report.info("Spreadsheet opened successfully.. "+str(self.current_spreadsheet.title))
            return True
        except Exception as e:
            self.error.error("Couldn't create the spreadsheet with title "+str(spreadsheet_name))
            self.error.error(e)
            return False

    def share_spreadsheet(self,spreadsheet: gspread.Spreadsheet = None, url : str = None, perm_type : str = None, role : str = None) -> bool:
        """
        If your email is otto@example.com you can share the newly created spreadsheet with yourself:
        sh.share('otto@example.com', perm_type='user', role='writer')
        See share() documentation for a full list of accepted parameters.
        :param spreadsheet:
        :param url:
        :param perm_type:
        :param role:
        :return:
        """
        if url and perm_type and role:
            try:
                if spreadsheet :
                    spreadsheet.share(url, perm_type = perm_type, role = role)
                else:
                    self.current_spreadsheet.share(url, perm_type = perm_type, role = role)
            except Exception as e:
                self.error.error("OOPs !!! couldn't share the sheet....")
                return False
            self.record.warning("Sheet shared to the "+ str(url) +" (perm_type = " + str(perm_type) +" )  ( role = "+ str(role) + ") ")
            self.report.warning("Sharing the sheet to the url " + str(url))
            self.record.warning("Sheet shared to the "+ str(url) +" (perm_type = " + str(perm_type) +" )  ( role = "+ str(role) + ") ")
            return True

        self.report.info("mention the parameters to share the spreadsheet...")

    def create_worksheet(self, worksheet_name : str = None, rows:int = 100, cols : int = 100) -> bool:
        """
        It creates the worksheet for the same spread sheet and parameters are given for the title
        and can returns nothingss....
        :param worksheet_name:
        :param rows:
        :param cols:
        :return:
        """
        if not worksheet_name:
            return False
        try:
            # *** create the work sheet with the given parameter....
            self.current_worksheet = self.current_spreadsheet.add_worksheet(title = worksheet_name, rows = rows, cols = cols)
            self.error.error(" New Worksheet Created by worksheetname : "+ str(worksheet_name))
            # *** creating a new model adaptor for the given worksheet
            # *** This modelAdaptor works with Worksheet , they make the crud operations easy
            # *** Those "CRUD" operations are discussed in the Adaptor Module....
            self.command_prompt += f"@{self.current_worksheet.title}"
            # *** setting the formatter to the handler
            self.consoleFormatter = log.Formatter(f" \033[0;40;8m {self.command_prompt} : %(levelname)s- %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
            self.consoleHandler.setFormatter(self.consoleFormatter)
            # *** Adding all the required Handlers....................
            self.report.info("Please Wait Adding Handlers...........")
            self.report.info("Handlers Added Succesfully............")
            self.report.info(f'Worksheet Opened @{self.current_worksheet.title}')
            return True
        except Exception as e:
            # *** if error in creating the worksheet than throw an Exceptio Error....
            self.error.error("Could not create the Worksheet on the worksheet Name  :  "+worksheet_name)
            self.error.error(e)
            return False

    def open_worksheet(self, title: str = None, index:int = None) -> bool:
        """
        it tries to open the work sheet from the spreadsheet
        :param title:  title of the worksheet to open and work with
        :param index:  index of worksheet in the spread sheet..
        :return:  bool
        """

        #*** open the worksheet by the title
        if title:
            try:
                self.current_worksheet = self.current_spreadsheet.worksheet(title)
            except gspread.WorksheetNotFound as e :
                self.error.error("No WorkSheet with Title "+ str(title))
                return False
        #*** open the worksheet by the index
        elif index:
            try:
                self.current_worksheet = self.current_spreadsheet.get_worksheet(index)
            except gspread.WorksheetNotFound as e :
                self.error.error("No WorkSheet with URL "+ str(index))
                return False
        else:
            try:
                self.current_worksheet = self.current_spreadsheet.sheet1
            except gspread.WorksheetNotFound as e :
                self.error.error("No WorkSheet Found............ ")
                return False
        # *** creating a new model adaptor for the given worksheet
        # *** This modelAdaptor works with Worksheet , they make the crud operations easy
        # *** Those "CRUD" operations are discussed in the Adaptor Module....
        self.success.debug(f"Worksheet Opened Successfully with Title  :: {self.current_worksheet.title} && url = {self.current_worksheet.url}")
        self.command_prompt += f"@{self.current_worksheet.title}"
        # *** setting the formatter to the handler
        self.consoleFormatter = log.Formatter(f"\033[0;40;8m {self.command_prompt} : %(levelname)s- %(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
        self.consoleHandler.setFormatter(self.consoleFormatter)
         # *** Adding all the required Handlers....................
        return True

    def delete_worksheet(self, worksheet : gspread.Worksheet = None) -> bool:
        """
        tries to Deletes the current worksheet....
        :param worksheet:  worksheet to be deleted...
        :return: bool
        """
        if (type(worksheet) != gspread.Worksheet or type(worksheet) == str) and worksheet != None:
            return False
        if worksheet:
            self.current_spreadsheet.del_worksheet(worksheet)
            self.current_worksheet = None
            self.record.warning("worksheet Deleted successfully " + str(self.current_worksheet))
            self.report.warning("worksheet Deleted successfully " + str(self.current_worksheet))
            return True
        else:
            try:
                self.current_spreadsheet.del_worksheet(self.current_worksheet)
                self.current_worksheet = None
                self.record.warning("worksheet Deleted successfully " + str(self.current_worksheet))
                cmd_roots = self.command_prompt.split("@")
                self.command_prompt = "@"+str(cmd_roots[0]) + "@"+str(cmd_roots[1])
                # *** setting the formatter to the handler
                self.consoleFormatter = log.Formatter(f" {self.command_prompt} : %(levelname)s- \033[0;3;8m%(message)s" ,datefmt='%Y-%m-%d => %H:%M ')
                self.consoleHandler.setFormatter(self.consoleFormatter)
                return True
            except Exception as e:
                self.report.error(e)
                return False
    @property
    def test_credentials(self):
        return r"D:\PYTHON TECHNOLOGY\PROJECTS\PySheetAdaptor Package\Credentials\CreatorCredentials.json"
    @property
    def test_spreadsheet_url(self):
        return r"https://docs.google.com/spreadsheets/d/13iG1TY1222nhtSumrO7J3hSUFloQM-qfQ4-OuH-YkVU/edit?usp=sharing"


