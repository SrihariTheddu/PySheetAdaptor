from setuptools import setup

setup(
    name = "PySheetAdaptor",
    version="3.8",
    description = "This package makes its easier to work with google spread sheets with by tracking your changes into a log file",
    long_description="""
    The main features of using this package is
    1. It tracks the changes made to the spreadsheet by using logging modules in python.
    2. You can save and manipulate data into different formats like csv, sql etc
    3. You can view your data as html format..
    4. You can backup your data if that particular log file exists
    """,
    author = "Theddu Srihari",
    packages = [r"PySheetAdaptor\Drivers","PySheetAdaptor"],
    install_requires = ["gspread", "oauth2client.service_account", "pandas", "numpy","matplotlib", "django", "sqlalchemy"]
)



















