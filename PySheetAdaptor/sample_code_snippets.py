"""
           THIS THE SAMPLE CODE SNIPPETS YOU NEED TO KNOW BEFORE USING.......
"""
#Import the Required Modules........
from PySheetAdaptor.PySheetAdaptor import PySheetAdaptor

# If you are running first time on the machine do not give any params..
# It will setup the environment and make all the requied configurations..
# you need to mention your googlesheet api credentials file as the path
# whenever it asks for the credentials..
adaptor = PySheetAdaptor()
# after executing above statement locally you will have created a local
# directory with following files......
# Dir :- guser\Credentials\user_credentials.json

## if you have already setup on local Machine you can use parametised constructor
## only if you want to automate the process
## You can skip the auto login process if you need....
# adaptor = PySheetAdaptor(AUTO_LOGIN = {"username":str,"password":str})

## if you want to create spreadsheet.....
## than open the spreadsheet ...........
# adaptor.create_spreadsheet(spreadsheet_name = str)

# if you spreadsheet created already than you can open it by providing the url of the spreadsheet
# opens the spreadsheet
# No Configurations done here...
adaptor.open_spreadsheet(url = adaptor.test_spreadsheet_url)


## if you want on new worksheet than create worksheet by using follwing method
## It creates the worksheet and setups for the worksheet....
# adaptor.create_worksheet(worksheet_name = str)
#
## if you have worksheet already than you can directly open the worksheet and setups the
## local machine to work...
## following dirs are created on your local machine on successfull setup
##  > guser
##         > credentials
##               user_credentials.json
##  > spreadsheetname
##       > worksheetname
##               > logBooks
##                       logbook_name
##               > Storage
##                       db_restore_name
adaptor.open_worksheet(
        title = "testsheet",
        logbook_name = "01-01-2021.txt",
        db_restore_name = "01-01-2021.txt"
        )


# After opening the worksheet now you can view data of the sheet..by just using the command
# It prints all the meta data.......
adaptor.__print__()

## *********************************************************************************************************************
## if you want to set the columns for the sheet you can do it by executing command
# Note that your column names must follow python convention variables
# latter those columns can be used python object attributes....
# adaptor.set_columns(columns = ["ID", "FirstName", "LastName", "Gender", "Age", "Address", "ContactNo"])
#

# *********************************************************************************************************************
#    *******************   ROW LEVEL OPERATIONS  ******************************

# If you want to insert record than you can used the following code snippet..
# by executing the following code the record is append at the end of worksheet..
# adaptor.insert_record(record = [100, "Dwayne", "Johnson", "Male", 52, "US", +50_90856575])

# If you want to insert record at partiular index than you can used the following code snippet..
# by executing the following code the record is append at the following index.
adaptor.insert_record(record = [100, "Dwayne", "Johnson", "Male", 52, "US", +50_90856575], index=1)

# For updating the record use the following code snippet...
# It updates the particular mentioned record if it exists...
adaptor.update_record(ID=100, updated_columns = ["ContactNo"], updated_values = [901453664])

# # For deleting the records the use the code snippet
# # This deletes the mentioned record from worksheet if exits
# adaptor.delete_record(ID=100)

# For retrieving the record u can use the below codesnippet...
print(adaptor.search_record(ID=100))
#
# # *********************************************************************************************************************
# #    *******************   COLUMN LEVEL OPERATIONS  ******************************
#
# # To Add an extra column to worksheet the following code snippet is used......
# ## adds an extra column with default values...
# adaptor.add_column(column_name = "TestColumn", column_values = [0]*adaptor.no_of_rows)
#
# # To delete the column use the code snippet
# # deletes the column if exists
# adaptor.delete_column(column_name = "TestColumn")


# *********************************************************************************************************************
#    *******************   TABLE LEVEL OPERATIONS  ******************************

# To save all the operations performed till now we need to commit
# It updates the changes locally....
adaptor.commit()
#
# #To undo all the operations we use rollback...........
# # undoes the changes made
# adaptor.rollback()


# *********************************************************************************************************************
#    *******************   SERVER LEVEL OPERATIONS  ******************************

## it uploads the updated data to the server sheet..
## all changes are affected on the server sheet....
adaptor.upload_to_server()



# *********************************************************************************************************************
#    *******************   SAVE CHANGES TO LOCAL FILES  ******************************

# # If you want to save the changes as file than use command...
# # save the data to the local file....
# adaptor.dump(destination_url = str)
#
# # save the changes as html file than use the code snippet
# adaptor.load_to_html()
#
# # To save as database use the code snippet
# adaptor.load_to_sql()


## finally we close the connection
adaptor.close_connection()


# # *********************************************************************************************************************
# #    *******************   BACK UP DATA AND CHECK LOGS.... *****************************************
#
# ## The following code is used to backup the data from the log files....
# from PySheetAdaptor.Drivers.BackUpDriver import  BackupDriver
# driver = BackupDriver(
#         filename = None,
#         files = [],
#         size = 1000
# )
# driver.config_data_from_files()
# driver.parse_data_as_restore()
# driver.dump(destination_url = str)
#
#
#
# ## The following code is used to config and check log files.....
# from PySheetAdaptor.Drivers.BackUpDriver import  BackupDriver
# driver = BackupDriver(
#         filename = None,
#         files = []
# )
# driver.config_data_from_files()
# driver.parse_as_logbook()
# driver.print_logs(driver.get_all_logs(key = str))




















