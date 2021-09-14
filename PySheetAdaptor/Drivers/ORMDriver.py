# Import all the required modules here...
from PySheetAdaptor.Drivers.PySheetDriver import PySheetDriver
import pandas as pd


class ORMDriver:
    """
    This Driver is used to convert the spreadsheet data into python objects to make work easier...
    """

    def __init__(self, driver: PySheetDriver, **kwargs):
        self.objectClass = None
        self.collections: list = []
        self.collections_count = 0
        self.attributes: list = []
        self.no_of_attributes = 0
        self.dataframe = None
        self.driver = driver
        self.name = kwargs.pop("name", driver.__name__)
        driver.installORMDriver(self)
        self.driver.report.info(f"""
          Object Related Mapper(ORM) Driver installed successfully.....
          ORMDriver : <{self.name}>
        """)
        self.get_default_class()
        self.set_class_attributes(self.driver.get_attributes)
        self.configure_driver()

    def get_default_class(self):
        class DefaultClass:
            def __init__(self, kwargs):
                for k,v in kwargs.items():
                    self.__setattr__(k,v)

        self.objectClass = DefaultClass
        return self.objectClass

    def set_class_attributes(self, attributes):
        self.attributes = attributes
        self.no_of_attributes = len(attributes)


    def configure_driver(self, **kwargs):
        self.objectClass = kwargs.pop("model", self.get_default_class())
        self.set_class_attributes(self.driver.get_attributes)
        for record in self.driver.records:
            self.generate_object(record_values = record, add_to_factory = True)
        self.driver.report.info(f"""
          Objects Mapped Successfully........
          Total No Of Objects      ::  {self.collections_count}
          No Of Attributes         ::  {self.no_of_attributes}
          ObjectClassModel  ::
                  {self.objectClass.__dict__}
        """)

    def update_to_driver(self):
        self.driver.records = self.get_all_values
        self.driver.reload()

    def uninstall_driver(self):
        self.driver.orm_driver = None

    def close_driver(self):
        self = None

    def generate_object(self, record_values = None, add_to_factory = True, **kwargs):
        obj_kwargs = {}
        if record_values:
            if len(record_values)!=len(self.attributes):
                return
            for index,attribute in enumerate(self.attributes):
                obj_kwargs[attribute] = record_values[index]
        else:
            for attribute in self.attributes:
                obj_kwargs[attribute] = kwargs.pop(attribute, None)
        curr_obj = self.objectClass(obj_kwargs)
        if add_to_factory:
            self.collections.append(curr_obj)
            self.collections_count += 1
        return curr_obj

    def delete_object(self, **kwargs):
        keys, values = [], []
        for key, value in kwargs.items():
            if key in self.attributes:
                keys.append(key)
                values.append(value)

        for index, curr_obj in enumerate(self.collections):
            for key, value in zip(keys, values):
                if getattr(curr_obj, key)!=value:
                    break
            else:
                self.collections.remove(self.collections[index])

    def search_object(self, **kwargs):
        keys, values = [], []
        for key, value in kwargs.items():
            if key in self.attributes:
                keys.append(key)
                values.append(value)

        for index, curr_obj in enumerate(self.collections):
            for key, value in zip(keys, values):
                if getattr(curr_obj, key)!=value:
                    break
            else:
                return self.as_values(curr_obj)


    def update_object(self, key, value, update_object):
        if key not in self.attributes:
            return
        for row in range(len(self.collections)):
            if self.collections[row].__getattribute__(key) == value:
                self.collections[row] = update_object
                return
        else:
            return False


    def as_values(self,model):
        values = []
        for attr in self.attributes:
            values.append(getattr(model,attr))
        return values

    @property
    def get_all_values(self):
        values = []
        for obj in self.collections:
            values.append(list(self.as_values(obj)))
        return values

    def get_as_dataframe(self):
        self.dataframe = pd.DataFrame(self.get_all_values,columns=self.attributes)
        return self.dataframe


















