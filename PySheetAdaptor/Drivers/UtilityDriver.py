6
import logging as log
from functools import reduce
from sys import stdout

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    stdout.flush()

def run_with_protected_environ(func, *args, **kwargs):

    def protected_method(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except Exception as e:
            self.error.error(self.error_message)
    return protected_method

def row_level_change(method, *args, **kwargs) -> None:

        def track_change(self, *args, **kwargs):
            exec_schema = method(self, *args, **kwargs)

            if exec_schema["Status"] == self.TRANSACTION_FAILED:
                return exec_schema
            # *** Retrieve the data from Keyword Arguments............
            schema_operation = exec_schema.pop("Operation")
            schema_index = exec_schema.pop("Index")
            schema_record = exec_schema.pop("Record")
            schema_change_record = exec_schema.pop("Updated Record")
            schema_action = exec_schema.pop("action")
            schema_reaction = exec_schema.pop("reaction")
            schema_url = exec_schema.pop("url")

            # *** Parse the message String......
            message = f"{schema_operation}-{schema_index}-" + str(reduce(lambda x, y: str(x)+":"+str(y), schema_record))
            message_id = schema_operation[0] + str(schema_index)

            if schema_operation == "Update":
                message += "->" + str(reduce(lambda x, y: str(x)+":"+str(y), schema_change_record))

            if len(self.messages[self.bp_cursor])==0:
                self.messages[self.bp_cursor].append((message_id, message, schema_action, schema_reaction, schema_url))
                return
            self.messages[self.bp_cursor].append((message_id, message, schema_action, schema_reaction, schema_url))
        return track_change

def batch_row_level_change(self,exec_schema):
    schema_operation = exec_schema.pop("Operation")
    schema_index = exec_schema.pop("Index")
    schema_record = exec_schema.pop("Record")
    schema_change_record = exec_schema.pop("Updated Record")
    schema_action = exec_schema.pop("action")
    schema_reaction = exec_schema.pop("reaction")
    schema_url = exec_schema.pop("url")

    # *** Parse the message String......
    message = f"{schema_operation}-{schema_index}-" + str(reduce(lambda x, y: str(x)+":"+str(y), schema_record))
    message_id = schema_operation[0] + str(schema_index)

    if schema_operation == "Update":
        message += "->" + str(reduce(lambda x, y: str(x)+":"+str(y), schema_change_record))

    if len(self.messages[self.bp_cursor])==0:
        self.messages[self.bp_cursor].append((message_id, message, schema_action, schema_reaction, schema_url))
        return
    self.messages[self.bp_cursor].append((message_id, message, schema_action, schema_reaction, schema_url))


@run_with_protected_environ
def column_level_change(method, *args, **kwargs):

        def track_change(self, *args, **kwargs):
            exec_schema = method(self, *args, **kwargs)
            if exec_schema["Status"] == self.TRANSACTION_FAILED:
                return exec_schema
            schema_operation = exec_schema.pop("Operation")
            schema_column = exec_schema.pop("Column Name")
            schema_action = exec_schema.pop("action")
            schema_reaction = exec_schema.pop("reaction")
            schema_column_values = exec_schema.pop("Column Values")
            schema_url = exec_schema.pop("url")
            message = f"{schema_operation}-{schema_column}-" + str(schema_column_values[0])
            message_id = "".join([s[0] for s in schema_operation.split(" ")])
            self.messages[self.bp_cursor].append((message_id, message, schema_action, schema_reaction, schema_url))

        return track_change

def table_level_change(method, *args, **kwargs):

       def track_change(self, *args, **kwargs):
            exec_schema = method(self, *args, **kwargs)
            if exec_schema["Status"] == self.TRANSACTION_FAILED:
                return exec_schema
            schema_operation = exec_schema.pop("Operation",None)
            if schema_operation == "Commit":
                if self.BOUNDED_ENVIRON:
                    if input("Please Verify once Again Commit[Y/N]   ::   ").lower() == 'n':
                        return
                for message in self.messages[self.bp_cursor]:
                    message[2][0](**message[2][1])
                    self.report.info(message[4])
                self.restore()
                self.messages.append([])
                self.bp_cursor += 1
                self.reload()
                self.success.warning("Committed successfully........")
            elif schema_operation == "RollBack":
                self.bp_cursor -= 1
                if self.BOUNDED_ENVIRON:
                    if input("Please Verify once Again Rollback[Y/N]   ::   ").lower() == 'n':
                        return
                for message in self.messages[self.bp_cursor]:
                    message[3][0](**message[3][1])
                    self.report.info("Restoring The Methods" +message[4])
                self.remove()
                self.success.warning("Roll back successfull....")
       return track_change

# =====================================================================================================================
## EXCEPTIONS ARE DEFINED HERE..................
class BaseException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class InvalidCredentialsException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"Couldn't build the Environment for dir ::{self.message}"

class AuthenticationException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"Authentication Failed ::{self.message}"

class TransitionException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"couldn't transit {self.message}"

class SourceEngineNotAvailableException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"::{self.message}\n Enter valid Source url....."

class DestinationEngineNotAvailableException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"::{self.message}\n Enter valid Destination url....."

class InvalidRecordException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"::{self.message} \n RecordIsImCompatible"

class InvalidColumnException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"::{self.message}\n NoColumnExists with GivenName"

class UploadError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"::{self.message} \n Unable to upload the data........."

class FileNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"::{self.message} \n Enter the valid File url........."

class SheetNotFoundException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"::{self.message}\n Forget to load the spreadsheet"

#======================================================================================================================
# ERRORS ARE DEFINED HERE.......
class BuildError(RuntimeError):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return f"Couldn't build the Environment for dir ::{self.message}"






