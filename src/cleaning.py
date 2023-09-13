import pandas as pd
import os

from typing import List

PWD = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PWD, "../data/")

ffill_columns = ["Date", "Exercise", "Variation", "Weight"]

def main():
    df = pd.read_csv(os.path.join(DATA_DIR, "data.csv"), index_col=0)
    # convert to upper case
    df = df.map(lambda x: x.upper() if isinstance(x, str) else x)
    # Remove trailing spaces from all string values
    df = df.map(lambda x: x.rstrip() if isinstance(x, str) else x)
    # fill 0 weight for selected Exercises
    # I was too lazy to fill in 0 when working out
    df.loc[(~df['Exercise'].isnull()) & (df["Weight"].isnull()), ['Weight']] = 0
    # forward fill
    [df[col].ffill(inplace=True) for col in ffill_columns]
    # convert str to datetime
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors='coerce')
    df.to_csv(os.path.join(DATA_DIR, "clean.csv"), index=False)

if __name__ == "__main__":
    main()