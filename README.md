# PySheetAdaptor

This is a python package which works with the google spreadsheet, csv files, xlsx files etc...
The main features of using this package is
* It logs the every change in the sheet to a file
* You can work with famous modules like pandas, numpy and matplotlib with your spreadsheet data...
* You can backup your sheet data if the particular state of log file exists..
* It has also a light weight django server where you can view your changes
* You can convert the sheet data into mysql and store, manipulate into database

Project structure:


    > PySheetAdaptor.py
    > client
          > GoogleClient.py
    > WebApp
          > webapp.py
    > PySheetResourceManager           
          > PySheetResourceManager.py
          > SystemAdmin.py
          > utils.py
          > Handlers.py
    > PySheetManager
          > PySheetManager.py
          > SheetAdaptor.py
    > tests
      

## PySheetAdaptor

 It authenticates the google user..
 This module interacts with the google spreadsheets
 It retrieves and updates the data onto the server..
 
 
## PySheetResourceManager
  
  It setups the copy of server data on the local machine and performs different operations on the sheet locally..
  The changes made locally are recorded in the log files by using logging handlers..
 
## PySheetManager
  
  It communicates with the local machine and setups the server copy on local machine'
  If local environment doesnot exist it uses SheetAdaptor to directly communicate with the sheet...
  
## Webapp

  It is the light weight django server runs on local machine.
 
 
#### for more info read the documentation
#### for architecture see the architecture.png





