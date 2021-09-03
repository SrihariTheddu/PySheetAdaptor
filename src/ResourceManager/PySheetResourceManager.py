##             ***         PYSHEET ADAPTOR         *****
## *** AN EFFICIENT MODULE TO WORK WITH WORKSHEETS............
## @Author       :: Theddu Srihari
## @EmailID      :: sriharitheddu02@gmail.com.....
## @Date         :: 11-09-2021
## Requirements  :: pandas, numpy, matplotlib, os, sys modules........
## Supported Versions..................................................
## github link ::
## ====================================================================================================================
## @Import Section(Imported Required Modules Here)


## ====================================================================================================================
## @Global Section.............................................
import math
from sys import getsizeof
from os import path
import pandas as pd
from pandas import DataFrame
from numpy import array
import sqlalchemy
import time
from PySheetAdaptor.src.ResourceManager.utils import row_level_change, column_level_change, table_level_change, run_with_protected_environ
from PySheetAdaptor.src.ResourceManager.Handlers import MainHandler
import csv
from PySheetAdaptor.src.ResourceManager.SystemAdmin import SystemAdmin
from PySheetAdaptor.src.exceptions import TransitionException
## ====================================================================================================================
class PySheetResourceManager(MainHandler, SystemAdmin):
    """
    It is an Python Adaptor used to work spreadsheets and excel sheets efficiently by using python modules....
    It has efficiently performs searching and writing operations as it uses the Indexing........
    For more info contact the above information.......
    """
    __name__: str
    source_name: str
    source_url: path
    destination_url: path
    destination_name: str
    dataframe: DataFrame
    records: list
    columns: list
    no_of_columns: int
    no_of_rows: int
    cursor: int
    indexes: array
    is_dumped: bool
    primary_key: str
    division_number: int
    division_counter: int
    index_pointers: list
    messages: list
    sql_engine: sqlalchemy.engine
    bp_cursor: int
    back_up_data: list
    command_prompt: str
    ## @Static Constants defined Here......
    SOURCE_NOT_FOUND: bool = False
    ERROR_IN_LOADING = False
    DESTINATION_NOT_FOUND = False
    ERROR_IN_DUMPING = False
    ARGUMENT_ERROR: int = False
    KEY_ERROR: bool = False
    ## If any operation performed successfully.......
    TRANSACTION_SUCCESS: int = 100
    TRANSACTION_FAILED: int = 101
    TRANSACTION_TERMINATED: int = 102
    RECORD_NOT_FOUND: int = False
    EMPTY_RECORD: int = False
    INVALID_INDEX: int = False
    INVALID_COLUMN: int = 200
    INVALID_RECORD_ERROR: dict = dict()



    def adaptor_setup(self, *args, **kwargs) -> object:
        """
        This constructor has No Arguments
        :param args:
        :param kwargs:
        """
        ## @Source variables........
        self.source_url: path = path
        self.source_name: str = str("")
        ## @Destination variables........
        self.destination_url: path = path
        self.destination_name: str = str("")
        ## @Setting utility variables........
        self.records: list = list()
        self.columns: list = list()
        self.no_of_columns: int = int(0)
        self.no_of_rows: int = int(0)
        self.cursor: int = int(0)
        self.is_dumped: bool = False
        # noinspection PyArgumentList
        self.indexes: array = array(10)
        self.primary_key: str = str("id")
        ## @Indexing Variables...
        self.division_number: int = int(30)
        self.division_counter: int = int(4)
        self.index_pointers: list = [int(0)] * self.division_number
        ## @Naming the Adaptor
        self.__name__: str = kwargs.pop("name", str(id(self)))
        ## @Manipulating Variables.......
        self.dataframe: DataFrame = DataFrame(self.records, columns=self.columns)
        self.sql_engine: sqlalchemy.engine = sqlalchemy.engine
        self.messages: list = [[], ]
        self.bp_cursor: int = 0
        self.back_up_data: list = []
        self.command_prompt: str = "@"
        super().__init__(*args, **kwargs)
        self.success.warning(f"<PySheetAdaptor : {self.__name__}> created successfully!!!")
        self.success.warning(f"<Memory Used : {getsizeof(self)} bytes at Address :: {id(self)}>")

    ## @verfies the source file......
    def load_from_file(self, source_url)-> bool:
        ## checking if path exists.....
        if path.isfile(source_url):
            self.source_url = source_url
            self.source_name = path.basename(self.source_url)
            self.report.debug(f"Loaded File Successfully from Source File ......")
            self.report.debug(f"Source Path   :: {self.source_url}")
            self.report.debug(f"Source Name :: {self.source_name}")
            self._load_()
            self._map_()
            return True
        self.error.error("Error in loading......")
        return self.ERROR_IN_LOADING

    ## Load from the Source filess.....
    @run_with_protected_environ
    def _load_(self) -> bool:
        ## If source is from csv file.........
        if self.source_name[-3:] == "csv":
            self.dataframe = pd.read_csv(self.source_url, index_col=None)
            self.report.debug(f"Loaded the Data into DataFrame..........")
            return True
        elif self.source_name[-2:] == 'db':
            self.sql_engine = sqlalchemy.create_engine(self.source_url)
            self.dataframe = pd.read_sql(f'SELECT * FROM {self.source_name}', self.sql_engine)
            self.report.debug("Requested for SQL Engine.....")
            self.report.debug(f"Creating SQL Engine ..........")
            self.report.debug(f"Memory alloted for Dataframe (read data) :: {getsizeof(self.dataframe)} bytes")
            return True
        else:
            try:
                self.dataframe = pd.DataFrame(self.current_worksheet.get_all_records())
                self.report.debug(f"Loaded Data successfully from Server url  :: {self.source_url}")
            except:
                self.error.error("Error in loading......")
                return self.SOURCE_NOT_FOUND


    def dump(self, destination_url=None, destination_name=None):
        #if path.isfile(destination_url):
        try:
            self.destination_url = destination_url
            if destination_name is None:
                self.destination_name = path.basename(self.destination_url)
            else:
                self.destination_name = destination_name
            self._dump_()
        except:
            self.error.error(f"No Destination Found with url  :: {self.destination_url}")

    #@run_with_protected_environ
    def _dump_(self):
        self.reload()
        if self.destination_name[-3:] == "csv":
            self.dataframe.to_csv(self.destination_name, encoding='utf-8', index=False)
            self.success.warning(f"Dumped to file successfully file url(csv): {self.destination_url}")
        elif self.destination_name[-4] == "xlsx":
            with pd.ExcelWriter(self.destination_name) as writer:
                self.dataframe.to_excel(writer)
            self.success.warning(f"Dumped to file successfully file url(excel): {self.destination_url}")
        else:
            self.error.error("Destination Engine Not Available...........")
            return
        self.success.error("Dumped Successfully ........")

    @run_with_protected_environ
    def manual_dump(self):
        with open(self.destination_name, "w", newline=" ") as f:
            writer = csv.writer(f)
            writer.writerow(self.columns)
            writer.writerows(self.records)


    def _map_(self):
        try:
            self.report.debug(f"Mapping the DataFrame -> Sheet")
            self.columns = list(self.dataframe.columns)
            self.no_of_columns = len(self.columns)
            # noinspection PyTypeChecker
            self.records = [self.columns, ]+list(self.dataframe.values.tolist())
            self.no_of_rows = len(self.records)
            self.cursor = int(self.no_of_rows)
            self.indexes = array([i for i in range(self.no_of_rows)])
            self.report.debug(f"Records loaded No of Records ::  {self.no_of_rows}")
            self.report.debug(f"Columns <columns>            ::  {self.columns}")
            self.report.debug(f"Memory Usage for Sheet  :: {getsizeof(self.records)} bytes")
            self.report.debug(f"Meta Data Created of {getsizeof(self.columns) + getsizeof(self.indexes) } bytes")
            self._refresh_()
        except:
            raise TransitionException("Error in configuring the data on local machine")

    @run_with_protected_environ
    def set_attributes(self, attributes):
        self.columns = attributes
        self.no_of_columns = len(attributes)
        if self.no_of_rows == 0:
            self.records.append(self.columns)
            self.cursor = 1
            self.no_of_rows = 1
        else:
            self.records[0] = self.columns
        self.report.debug(f"TableLevelSchema <AddToQueue> <Add columns <{self.columns}><Intlength :{self.no_of_columns}")

    @property
    def get_attributes(self):
        return self.columns

    @run_with_protected_environ
    def reload(self):
        self.dataframe = pd.DataFrame(self.records, columns=self.columns)
        self.no_of_rows = len(self.records)
        self.cursor = int(self.no_of_rows)
        self.no_of_columns = len(self.columns)
        self.records[0] = self.columns
        self.indexes = array([i for i in range(self.no_of_rows)])
        self.report.debug(f"Records loaded No of Records ::  {self.no_of_rows}")
        self.report.debug(f"Columns <columns>            ::  {self.columns}")
        self.report.debug(f"Memory Usage for Sheet  :: {getsizeof(self.records)} bytes")
        self.report.debug(f"Meta Data Created of {getsizeof(self.columns) + getsizeof(self.indexes) } bytes")
        self._refresh_()

    def _refresh_(self):
        self.division_counter = math.ceil(self.no_of_rows/self.division_number)
        for index in range(self.division_number):
            self.index_pointers[index] = self.division_counter*index

    def get_index(self, keys: list, values: list) -> int:
        if len(keys) != len(values):
            return -1
        key_indexes: list = []
        for key in keys:
            key_indexes.append(self.columns.index(key))
        for index in range(self.no_of_rows):
            for key, value in zip(key_indexes, values):
                if self.records[index][key] != value:
                    break
            else:
                return index
        return self.RECORD_NOT_FOUND

    ## ================================================================================================================
    ##  ROW LEVEL SCHEMAS ARE HERE...............
    @run_with_protected_environ
    def __insert__(self, **kwargs):
        record = kwargs.pop("record", self.RECORD_NOT_FOUND)
        index = kwargs.pop("index", 0)
        if index == 0:
            self.records.append(record)
            self.error.error(f"RowLevelSchema :: ExecutedFromQueue <InsertRecord::Record><{record}> at Index<{self.no_of_rows}>")
        else:
            self.records.append(record)
            self.report.info(f"RowLevelSchema :: ExecutedFromQueue <InsertRecord::Record><{record}> at Index<{index}>")
        self.no_of_rows += 1

    @row_level_change
    def _insert_(self, **kwargs) -> dict:
        # *** Retrieve Args to process...
        record = kwargs.pop("record", self.RECORD_NOT_FOUND)
        position = int(kwargs.pop("position", 0))
        # if Empty Record Return Nothing
        if record == self.RECORD_NOT_FOUND:
            self.error.error(f"RowLevelSchema :: Failed ToAddQueue/InsertRecord/record={record}&&RECORD_NOT_FOUND>")
            return {"status": self.TRANSACTION_FAILED}
        # if no index than append in data buffer.......
        if position == 0:
            action = (self.__insert__, {"record": record})
            reaction = (self.__delete_record__, {"record": record})
            self.report.error(f"RowLevelSchema :: AddedToQueue <InsertRecord::Record><{record}> at Index<{self.cursor}>")
        else:
            action = (self.__insert__, {"record": record, "index": position})
            reaction = (self.__delete_record__, {"record": record})
            self.report.debug(f"RowLevelSchema :: AddedToQueue <InsertRecord::Record><{record}> at Index<{position}>")
        self.cursor += 1
        return {
            "Schema": "Row Level Schema",
            "Status": self.TRANSACTION_SUCCESS,
            "Operation": "Insert",
            "Index": self.cursor,
            "Record": record,
            "Updated Record": None,
            "action": action,
            "reaction": reaction,
            "url": f"/{self.source_name}/records/index={self.cursor}/append/"
        }

    #@run_with_protected_environ
    def _search_record_(self, **kwargs) -> object:
        keys = kwargs.pop("keys", self.ARGUMENT_ERROR)
        values = kwargs.pop("values", self.ARGUMENT_ERROR)
        # *** get the index of record using utility functions........
        index = self.get_index(keys=keys, values=values)
        if index == self.RECORD_NOT_FOUND:
            self.error.error(f"Record Not Found/{str([ key+'='+value+'&&' for key,value in zip(keys, values)])}<KEY_ERROR>")
            return self.RECORD_NOT_FOUND
        return self.records[index]

    # *** Updated the Record with given params.........
    #Tested Successfully...........
    @run_with_protected_environ
    def __update__(self, **kwargs):
        record = kwargs.pop("record", self.RECORD_NOT_FOUND)
        index = kwargs.pop("index", self.ARGUMENT_ERROR)
        self.records[index] = record
        self.report.info(f"RowLevelSchema :: ExecutedFromQueue <UpdateRecord::Record><{record}> at Index<{self.cursor}>")

    @row_level_change
    def _update_(self, **kwargs) -> dict:
        # *** Retrieve the data args to process......
        updated_columns = kwargs.pop("updated_columns", self.INVALID_COLUMN)
        updated_values = kwargs.pop("updated_values" , self.EMPTY_RECORD)
        keys = kwargs.pop("keys", self.ARGUMENT_ERROR)
        values = kwargs.pop("values", self.ARGUMENT_ERROR)
        # *** get the index of record using utility functions........
        index = self.get_index(keys=keys, values=values)
        # *** if No Record Found Return Transaction Failed........
        if index == self.RECORD_NOT_FOUND or index == -1:
            self.error.error(f"RowLevelSchema :: Failed ToAddQueue/UpdateRecord/{str([ key+'='+value+'&&' for key,value in zip(keys, values)])}<KEY_ERROR>")
            return {"Status": self.TRANSACTION_FAILED}
        # *** else If Record Found.....
        old_record: list = self.records[index]
        new_record: list = list(old_record)
        # *** Update all the values in the Record.................
        for idx, column in enumerate(updated_columns):
                new_record[self.columns.index(column)] = updated_values[idx]
        action = (self.__update__, {"record": new_record, "index": index})
        reaction = (self.__update__, {"record": old_record, "index": index})
        self.report.debug(f"RowLevelSchema :: AddedToQueue <UpdateRecord::Record><{new_record}> at Index<{index}>")
        # *** Return the Output schema............
        return {
            "Schema": "Row Level Schema",
            "Status": self.TRANSACTION_SUCCESS,
            "Operation": "Update",
            "Index": index,
            "Record": old_record,
            "Updated Record": new_record,
            "action": action,
            "reaction": reaction,
            "url": f"/{self.source_name}/records/{str([ key+'='+value+'&&' for key,value in zip(keys, values)])}/update/"
        }

    @run_with_protected_environ
    def __delete_record__(self, **kwargs):
        record: list = kwargs.pop("record", self.RECORD_NOT_FOUND)
        index: int = kwargs.pop("index", self.INVALID_INDEX)
        self.records.remove(record)
        self.no_of_rows -= 1
        self.report.info(f"RowLevelSchema :: ExecutedFromQueue <DeleteRecord::Record><{record}> at Index<{self.no_of_rows+1}>")

    @row_level_change
    def _delete_(self, **kwargs):
        keys = kwargs.pop("keys", self.ARGUMENT_ERROR)
        values = kwargs.pop("values", self.ARGUMENT_ERROR)
        # *** get the index of record using utility functions........
        index = self.get_index(keys=keys, values=values)
        # *** If No Record Exists..........
        if index == self.RECORD_NOT_FOUND:
            self.error.error(f"RowLevelSchema :: Failed ToAddQueue/DeleteRecord/{str([ key+'='+value+'&&' for key,value in zip(keys, values)])}>")
            return {"Status": self.TRANSACTION_FAILED}
        # *** If Found then locate the schema..........
        record = list(self.records[index])
        # *** drop the row........
        action = (self.__delete_record__, {"record": record})
        reaction = (self.__insert__, {"record": record, "index": index})
        self.report.debug(f"RowLevelSchema :: AddedToQueue <DeleteRecord::Record><{record}> at Index<{index}>")
        self.cursor -= 1
        return  {
            "Schema": "Row Level Schema",
            "Status": self.TRANSACTION_SUCCESS,
            "Operation": "Delete",
            "Index": index,
            "Record": record,
            "Updated Record": None,
            "action": action,
            "reaction": reaction,
            "url": f"/{self.source_name}/records/{str([ key+'='+value+'&&' for key,value in zip(keys, values)])}/delete/"
        }

    ## ================================================================================================================
    ##  COLUMN LEVEL SCHEMAS
    # *** add the column.............
    @run_with_protected_environ
    def __add_column__(self, **kwargs):
        column_name = kwargs.pop("column_name", self.ARGUMENT_ERROR)
        column_values = kwargs.pop("column_values", self.ARGUMENT_ERROR)
        for idx, col_value in zip(range(1, self.no_of_rows), column_values):
            self.records[idx].append(col_value)
        # Adding column ......................
        self.columns.append(column_name)
        self.records[0].append(column_name)
        self.no_of_columns += 1
        self.report.info(f"ColumnLevelSchema :: ExecutedFromQueue AddColumn/column={column_name}/ ")

    @column_level_change
    def _add_column_(self, **kwargs) -> dict:
        # *** Retrieve the Data from arguments......
        column_name = kwargs.pop("column_name", self.ARGUMENT_ERROR)
        column_values = kwargs.pop("column_values", self.ARGUMENT_ERROR)
        # *** Checking if Valid Column Name....
        if column_name == self.ARGUMENT_ERROR or column_name in self.columns:
            self.error.error(f"ColumnLevelSchema :: Failed ToAddQueue <AddColumn::Column><{column_name}>")
            return {"Status": self.TRANSACTION_FAILED}
        action = (self.__add_column__, {"column_name": column_name, "column_values": column_values})
        reaction = (self.__delete_column__, {"column_name": column_name})
        self.report.debug(f"ColumnLevelSchema :: AddedToQueue <AddColumn::Column><{column_name}>")
        # *** returning the schema............
        return {
            "Schema ": "Column Level Schema",
            "Status": self.TRANSACTION_SUCCESS,
            "Operation": "Add Column",
            "Column Name": column_name,
            "Column Values": column_values,
            "action": action,
            "reaction": reaction,
            "url": f"/{self.source_name}/column_name={column_name}/add/all/"
        }

    @run_with_protected_environ
    def __delete_column__(self, **kwargs):
        column_name = kwargs.pop("column_name", self.ARGUMENT_ERROR)
        column_index = kwargs.pop("column_index", self.ARGUMENT_ERROR)
        for idx in range(self.no_of_rows):
            self.records[idx].remove(self.records[idx][column_index])
        self.no_of_columns -= 1
        self.columns.remove(column_name)
        self.report.info(f"ColumnLevelSchema :: ExecutedFromQueue <DeleteColumn::Column><{column_name}>")

    @column_level_change
    def _delete_column_(self, **kwargs) -> dict:
        # *** Retrieve the Data from arguments......
        column_name = kwargs.pop("column_name", self.ARGUMENT_ERROR)
         # *** Checking if Valid Column Name....
        if column_name == self.ARGUMENT_ERROR or column_name not in self.columns:
            self.error.error(f"ColumnLevelSchema :: Failed ToAddQueue <DeleteColumn::Column><{column_name}>")
            return {"Status": self.TRANSACTION_FAILED}
        column_index = self.columns.index(column_name)
        column_values = []
        for idx in range(0, self.no_of_rows-1):
            column_values.append(self.records[idx][column_index])
        action = (self.__delete_column__, {"column_name": column_name, "column_index": column_index})
        reaction = (self.__add_column__, {"column_name": column_name, "column_values": column_values})
        self.report.debug(f"ColumnLevelSchema :: AddedToQueue <DeleteColumn::Column><{column_name}>")
        return {
            "Schema ": "Column Level Schema",
            "Status": self.TRANSACTION_SUCCESS,
            "Operation": "Remove Column",
            "Column Name": column_name,
            "Column Values": column_values,
            "action": action,
            "reaction": reaction,
            "url": f"/{self.source_name}/column_name={column_name}/remove/all/"
        }

    @table_level_change
    def _commit_(self, *args):
        self.report.debug(f"committing the previous changes........")
        return {
            "Schema ": "Table Level Schema",
            "Status": self.TRANSACTION_SUCCESS,
            "Operation": "Commit",
        }

    @table_level_change
    def _rollback_(self, *args):
        return {
            "Schema ": "Table Level Schema",
            "Status": self.TRANSACTION_SUCCESS,
            "Operation": "RollBack",
        }

    def clear_environ(self):
        self.report.debug("Cleaning the Environment.........")
        self.dataframe = DataFrame()
        self.records = []
        self.columns = []
        self.no_of_columns = 0
        self.no_of_rows = 0
        self.indexes = array(25)
        self.cursor = 0
        self.messages = [[],]
        self.bp_cursor = 0
        self.report.debug("Clear...........................")

    ## @Prints the Detailed Information of Object.............
    @run_with_protected_environ
    def __print__(self):
        start = time.perf_counter()
        print(f"Source url  ::  {self.source_url}")
        print(f"Source Name  ::  {self.source_name}")
        print("-"*110)

        print(self.dataframe)
        print("-"*110)

        print(f"No of Rows      :: {self.no_of_rows}",end="  |  ")
        print(f"No of Columns   :: {self.no_of_columns}",end = "  |  ")
        print(f"Cursor Position :: {self.cursor}", end = "  |  ")
        print(f"Dumped :: {self.is_dumped}", end = "  |  ")
        print()
        print("-"*110)
        print("Memory Usage  :: ")
        dataframe = getsizeof(self.dataframe)
        records = getsizeof(self.records)
        meta = getsizeof(self.indexes) + getsizeof(self.columns) + getsizeof(self.cursor)*3
        baseobject = getsizeof(self.__dict__)
        print(f"DataFrame   : {dataframe} bytes  | Sheet  : {records} bytes  |  Meta Data : {meta} bytes ",end = " | ")
        print(f"Reference Base Object : {baseobject} bytes")
        total = (dataframe + records + meta + baseobject)/(1000)
        print(f"Total Memory Used  : {total} kb")
        print("-"*110)
        end = time.perf_counter()
        print(f"Processor Time :: {end-start:0.4f} seconds")
        print("-"*110)


    @property
    def meta_data(self):
        dataframe = getsizeof(self.dataframe)
        records = getsizeof(self.records)
        baseobject = getsizeof(self.__dict__)
        meta = getsizeof(self.indexes) + getsizeof(self.columns) + getsizeof(self.cursor)*3
        total = (dataframe + records + meta + baseobject)/(1000)
        return f"""
        Source url  ::  {self.source_url}
        Source Name  ::  {self.source_name}
        No of Rows      :: {self.no_of_rows}
        No of Columns   :: {self.no_of_columns}
        Cursor Position :: {self.cursor}
        Dumped :: {self.is_dumped}
        dataframe :: {dataframe}
        records :: {records}
        Meta  :: {meta}
        Total Data ::  {total}
        """





    def __repr__(self):
        return f"<PySheetAdaptor : {self.__name__}><id : {id(self)}>"
## ====================================================================================================================
##  ****************************************      THE END       *************************************************






















