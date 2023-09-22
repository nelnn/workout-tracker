import datetime
import numpy as np
import os
import pandas as pd
import gspread
import streamlit as st
from google.oauth2.service_account import Credentials


URL = "https://docs.google.com/spreadsheets/d/1AHD9Yhyi72-SfFkYtP6STqCKblk9ipkFOOVPnaQbCQE"


scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]

skey = st.secrets["gcp_service_account"]
credentials = Credentials.from_service_account_info(
    skey,
    scopes=scopes,
)
client = gspread.authorize(credentials)


# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(url=URL, sheet_name="Record"):
    sh = client.open_by_url(url)
    df = pd.DataFrame(sh.worksheet(sheet_name).get_all_records())
    df = df.replace(r"^\s*$", np.nan, regex=True)
    return df



PWD = os.path.dirname(os.path.abspath(__file__))
TIMESTAMP_DIR = os.path.join(PWD, "updated_timestamp.py")


def get_raw_data() -> list[pd.DataFrame, pd.DataFrame]:
    """
    Fetch workout and bodyweight data from Google Sheets and return as DataFrames.
    """
    try:
        # default location:
        # C:\Users\nsc\AppData\Roaming\gspread\credentials.json
        gc = gspread.service_account()
    except FileNotFoundError:
        gc = gspread.service_account(filename="service_account.json")
    sh = gc.open("Workout")
    workout = sh.worksheet("Record")
    df_raw = pd.DataFrame(workout.get_all_records())
    weight = sh.worksheet("Weight")
    df_bw = pd.DataFrame(weight.get_all_records())

    # replace blank spaces with Nan
    df_raw = df_raw.replace(r"^\s*$", np.nan, regex=True)
    df_bw = df_bw.replace(r"^\s*$", np.nan, regex=True)
    return df_raw, df_bw


def update_timestamp():
        with open(TIMESTAMP_DIR, "w") as fp:
            fp.write(f'"Updated {str(datetime.datetime.now(datetime.timezone.utc))}"\n')

if __name__ == "__main__":
     update_timestamp()