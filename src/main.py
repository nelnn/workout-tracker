import pandas as pd
import pickle
import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1AHD9Yhyi72-SfFkYtP6STqCKblk9ipkFOOVPnaQbCQE'
RANGE_NAME = 'Sheet1!A2:E'
DATA_TO_PULL = '2023'

PWD = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PWD, "../data/")

file_name = "data.csv"
SAVE_DIR = os.path.join(DATA_DIR, file_name)

def gsheet_api_check(SCOPES):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def pull_sheet_data(SCOPES,SPREADSHEET_ID, DATA_TO_PULL):
    creds = gsheet_api_check(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=DATA_TO_PULL).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                  range=DATA_TO_PULL).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data

if __name__ == '__main__':
    data = pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL)
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_csv(SAVE_DIR)