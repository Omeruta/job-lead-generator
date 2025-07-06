import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def upload_to_gsheet(dataframe, sheet_name, creds_path, sheet_id):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)

    sheet.clear()  # Remove old data
    sheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())

