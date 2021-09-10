# PySheetAdaptor

This is a python package which works with the google spreadsheet, csv files, xlsx files etc...
The main features of using this package is
* It logs the every change in the sheet to a file
* You can work with famous modules like pandas, numpy and matplotlib with your spreadsheet data...
* You can backup your sheet data if the particular state of log file exists..
* It has also a light weight django server where you can view your changes
* You can convert the sheet data into mysql and store, manipulate into database

Project structure:


    > Drivers
       > BackupDriver.py
       > MainDriver.py
       > PySheetDriver.py
       > SystemAdminDriver.py
       > UtilityDriver.py
       > WebAppDriver.py
   > tests
       > __init__.py
   > __init__.py
   > PySheetAdaptor.py
      

## PySheetAdaptor

 It authenticates the google user..
 This module interacts with the google spreadsheets
 It retrieves and updates the data onto the server..
 
 
## MainDriver
  
  It setups the copy of server data on the local machine and performs different operations on the sheet locally..
  The changes made locally are recorded in the log files by using logging handlers..
 
## PySheetDriver
  
  It communicates with the local machine and setups the server copy on local machine'
  If local environment doesnot exist it uses SheetAdaptor to directly communicate with the sheet...
  
## WebAppDriver

  It is the light weight django server runs on local machine.
 
 
#### for more info read the documentation
#### for architecture see the architecture.png





