
from os import path, getcwd
import pandas as pd
import sqlalchemy
from PySheetAdaptor.Drivers.MainDriver import MainDriver
from PySheetAdaptor.Drivers.UtilityDriver import InvalidColumnException, InvalidRecordException, SheetNotFoundException
## ====================================================================================================================
class PySheetDriver(MainDriver):

    def __init__(self):
        self.orm_driver = None
        super(MainDriver, self).__init__()

    def load_from_server(self)-> bool:
        if self.SERVER_SHEET:
            self.source_url = str(self.current_worksheet.url)
            self.source_name = str(self.current_worksheet.title)
            self.dataframe = pd.DataFrame(self.current_worksheet.get_all_records())
            if super()._map_():
                self.report.debug(f"""
                Loaded File Successfully from Source File .....
                Source Path   :: {self.source_url}
                Source Name :: {self.source_name}
                """
                )
                return True
        else:
            raise SheetNotFoundException("SpreadSheet not loaded.....")

    def installORMDriver(self, driver):
        self.orm_driver = driver

    def insert_record(self, record, index = None):
        if len(record) != self.no_of_columns:
            raise InvalidRecordException("No of columns doesn't match")
        self._insert_(record=record, index=index)

    def search_record(self, **kwargs):
        keys, values = [], []
        for key, value in kwargs.items():
            if key in self.columns:
                keys.append(key)
                values.append(value)
        return super()._search_record_(keys=keys, values=values)

    def update_record(self,updated_columns, updated_values,**kwargs):
        keys, values = [], []
        for key, value in kwargs.items():
            if key in self.columns:
                keys.append(key)
                values.append(value)
        self._update_(keys=keys, values=values, updated_columns=updated_columns, updated_values=updated_values)

    def delete_record(self, **kwargs):
        keys, values = [], []
        for key, value in kwargs.items():
            if key in self.columns:
                keys.append(key)
                values.append(value)
        self._delete_(keys=keys, values=values)

    def delete_all_record(self, **kwargs):
        keys, values = [], []
        for key, value in kwargs.items():
            if key in self.columns:
                keys.append(key)
                values.append(value)
        self._delete_all_(keys=keys, values=values)

    def add_column(self, column_name, column_values):
        if column_name in self.columns:
            raise InvalidColumnException("Column already exists....")
        print(self.__add_column__)
        super().add_column(column_name=column_name, column_values=column_values)

    def delete_column(self, column_name):
        if column_name not in self.columns:
            raise InvalidColumnException("Column doesn't exists....")
        self._delete_column_(column_name=column_name)

    def commit(self):
        self._commit_()

    def rollback(self):
        self._rollback_()

    def get_schemas(self):
        for messages in self.messages:
            for message in messages:
                print(message)
    @property
    def get_dataframe_description(self, **kwargs):
        try:
            return self.dataframe.describe(**kwargs)
        except TypeError :
            return self.dataframe(None)

    #=========================================================================================================
    # *** Load to the different Engines.................

    def load_to_sql(self, **kwargs) -> sqlalchemy.engine:
        self.sql_engine = sqlalchemy.create_engine('sqlite://', echo=False)
        self.dataframe.to_sql(kwargs.pop("table_name", self.source_name), con=self.sql_engine)
        self.success.warning(f"SQL engine created successfully Table Name :: {kwargs.pop('table_name', self.source_name)}")
        self.report.warning("Work Reference :: {class_name.sql_engine}")
        return self.sql_engine

    def load_to_html(self, **kwargs):
        file_path = kwargs.pop("file_path", getcwd())
        if self.source_name == "":
            self.source_name = "test"
        file_name = kwargs.pop("file_name", self.source_name[:-3] +".html")
        file_url = path.join(file_path, file_name)
        with open(file_url, "w") as html_writer:
            html_writer.write(self.dataframe.to_html())
        self.success.warning(f"HTML file downloaded successfully {self.base_html}")

    def write_html(self):
        with open(self.base_html, "w") as html_writer:
            html_writer.write(self.dataframe.to_html())

    def insert_to_sheet(self, record, position = None):
        if record is None or len(record)==0:
            return
        try:
            if position is not None:
                self.current_worksheet.insert_row(record,self.cursor)
            else:
                self.current_worksheet.append_row(record)
            self.cursor += 1
            self.report.info(f"@{self.current_worksheet.title} : Inserting values at {self.cursor-1} values{record}")
            return True
        except Exception as e:
            self.report.debug(f"{self.adaptor.current_worksheet.title}"+str(e)+f" Could not insert the record at position {position} record {record}")
            return False

    def append_to_sheet(self, records:list):
        if records is not None:
            try:
                self.current_worksheet.append_rows(records)
                self.cursor += len(records)
                self.report.info(f"@{self.current_worksheet.title} : Inserting values at {self.cursor} values{records}")
                return True
            except Exception as e:
                self.report.debug(f"{self.adaptor.current_worksheet.title}"+str(e)+f" Could not insert the record at position {self.index} record {records}")
                return False

    def update_to_sheet(self, key:str,attribute:str = None, record:list=[] ):
        index = self.get_index(keys=[attribute],values=[key])
        if index == -1:
            return False
        try:
            if index is not None:
                self.current_worksheet.insert_row(record,index)
            self.report.info(f"@{self.current_worksheet.title} : Updating values at {index} values{record}")
            return True
        except Exception as e:
            self.report.debug(f"{self.adaptor.current_worksheet.title}"+str(e)+f" Could not update the record at position {index} record {record}")
            return False

    def delete_from_sheet(self, key, value):
        index = self.get_index(keys=[key],values=[value])
        if index == -1:
            return False
        try:
            record = self.current_worksheet.get(index)
            self.current_worksheet.delete_row(index)
            self.report.info(f"@{self.current_worksheet.title} : Deleting values at {index} values{record}")
            return True
        except Exception as e:
            self.report.debug(f"{self.adaptor.current_worksheet.title}"+str(e)+f" Could not delete the record at position {index} record {record}")
            return False

    def drop(self):
        # *** drops the entire table including the attributes....
        self.current_worksheet.delete_rows(start_index = 1, end_index= self.cursor-1)

    def delete_columns_from_sheet(self, columns:list):
        for column in columns:
            index = self.columns.index(column)
            self.current_worksheet.delete_dimension("COLUMNS", index, None)

    def __repr__(self):
        return f"<PySheetAdaptor : {self.__name__}><id : {id(self)}>"
## ====================================================================================================================
##  ****************************************      THE END       *************************************************


























