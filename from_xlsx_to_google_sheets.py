from google.oauth2.service_account import Credentials
import gspread
import pandas as pd
from gspread_pandas import Spread, Client

CREDENTIALS = 'filepath_to_json_file'
SHEET = 'sheet_name'
EXCEL_FILE = 'path_to_excel_file'
scopes = ('https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive')

credentials = Credentials.from_service_account_file(CREDENTIALS, scopes=scopes)
df = pd.read_excel(EXCEL_FILE)
client = Client(scope=scopes, creds=credentials)
spread = Spread('1', client=client)
spread.df_to_sheet(df, index=False, sheet='New', start='A1', replace=True)






