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
from os import path, getcwd
import sqlalchemy
from PySheetAdaptor.src.ResourceManager.PySheetResourceManager import PySheetResourceManager
from PySheetAdaptor.src.Manager.SheetAdaptor import SheetAdaptor
## ====================================================================================================================
class PySheetManager(PySheetResourceManager, SheetAdaptor):
    """
    It is an Python Adaptor used to work spreadsheets and excel sheets efficiently by using python modules....
    It has efficiently performs searching and writing operations as it uses the Indexing........
    For more info contact the above information.......
    """
    source_url: str
    source_name: str

    def adaptor_setup(self, *args, **kwargs) -> None:
        super().adaptor_setup(*args, **kwargs)
        self.report.debug(f"Manager Setup successfully ")
        self.report.debug(f"Base Resources allocated Successfully.........")

    def load_from_source(self, source_url)-> bool:
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

    def insert_record(self, record):
        if len(record) != self.no_of_columns:
            return self.INVALID_RECORD_ERROR
        self._insert_(record=record)

    def search_record(self, **kwargs):
        keys, values = [], []
        for key, value in kwargs.items():
            if key in self.columns:
                keys.append(key)
                values.append(value)
        super()._search_record_(keys=keys, values=values)

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

    def add_column(self, column_name, column_values):
        self._add_column_(column_name=column_name, column_values=column_values)

    def delete_column(self, column_name):
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

    def load_to_sql(self, **kwargs):
        self.sql_engine = sqlalchemy.create_engine('sqlite://', echo=False)
        self.dataframe.to_sql(kwargs.pop("table_name", self.source_name), con=self.sql_engine)
        self.success.warning(f"SQL engine created successfully Table Name :: {kwargs.pop('table_name', self.source_name)}")
        self.report.warning("Work Reference :: {class_name.sql_engine}")

    def load_to_html(self, **kwargs):
        file_path = kwargs.pop("file_path", getcwd())
        if self.source_name == "":
            self.source_name = "test"
        file_name = kwargs.pop("file_name", self.source_name[:-3] +".html")
        file_url = path.join(file_path, file_name)
        with open(file_url, "w") as html_writer:
            html_writer.write(self.dataframe.to_html())
        self.success.warning(f"HTML file downloaded successfully........")


    def write_html(self):
        with open(self.base_html, "w") as html_writer:
            def color_negative_red(val):
                color = 'blue' if val > 90 else 'black'
                return 'color: % s' % color
            #self.dataframe.style.applymap(color_negative_red)
            html_writer.write(self.dataframe.to_html())

    def __repr__(self):
        return f"<PySheetAdaptor : {self.__name__}><id : {id(self)}>"
## ====================================================================================================================
##  ****************************************      THE END       *************************************************


























