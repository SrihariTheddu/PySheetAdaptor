import gspread
from oauth2client.service_account import ServiceAccountCredentials, client
import pandas as pd
import numpy as np
import os
import sys
import logging as log
import json
import math
from functools import reduce
import django
