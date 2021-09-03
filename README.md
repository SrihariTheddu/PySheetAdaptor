# PySheetAdaptor

This is a python package which works with the google spreadsheet, csv files, xlsx files etc...
The main features of using this package is
* It logs the every change in the sheet to a file
* You can work with famous modules like pandas, numpy and matplotlib with your spreadsheet data...
* You can backup your sheet data if the particular state of log file exists..
* It has also a light weight django server where you can view your changes
* You can convert the sheet data into mysql and store, manipulate into database

Project structure:


    PySheetAdaptor.py
    client
      GoogleClient.py
    WebApp
      webapp.py
    PySheetResourceManager
      PySheetResourceManager.py
      SystemAdmin.py
    PySheetManager
      PySheetManager.py
      SheetAdaptor.py
      









