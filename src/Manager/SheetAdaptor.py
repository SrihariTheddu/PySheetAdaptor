
class SheetAdaptor:

    def insert(self, record, position = None):

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


    def append(self, records:list):
        if records is not None:
            try:
                self.current_worksheet.append_rows(records)
                self.cursor += len(records)
                self.report.info(f"@{self.current_worksheet.title} : Inserting values at {self.cursor} values{records}")
                return True
            except Exception as e:
                self.report.debug(f"{self.adaptor.current_worksheet.title}"+str(e)+f" Could not insert the record at position {self.index} record {records}")
                return False


    def update(self, key:str,attribute:str = None, record:list=[] ):
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

    def delete(self, key, value):
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

    def delete_columns(self, columns:list):
        """Deletes multiple columns from the worksheet at the specified index.
        :param int start_index: Index of a first column for deletion.
        :param int end_index: Index of a last column for deletion.
            When end_index is not specified this method only deletes a single
            column at ``start_index``.
        """
        for column in columns:
            index = self.columns.index(column)
            self.current_worksheet.delete_dimension("COLUMNS", index, None)



































