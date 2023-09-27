import pandas as pd
import numpy as np
import os

PWD = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PWD, "../data/data.csv")


class Processing:
    def __init__(self, df_raw: pd.DataFrame) -> None:
        self.df_raw = df_raw
        self.df_raw_filled = self.get_filled_df()
        self.df_non_band, self.df_band = self._general_processing()

    def _general_processing(self) -> pd.DataFrame:
        df = self.df_raw_filled

        # select exercises with assistant bands
        assistant_band_exercises = df["Weight"].apply(str).str.isalpha()
        assistant_band_exercises = df[assistant_band_exercises]["Exercise"].unique()
        df_band = df[df["Exercise"].isin(assistant_band_exercises)]

        exercises_band = df_band["Exercise"].unique()
        df_non_band = df[~df["Exercise"].isin(exercises_band)]

        # purple, black, green, orange
        band_colour_mapping = {"P": 0.8, "B": 0.6, "G": 0.2, "O": 0.1}
        df_band = df_band.replace({"Weight": band_colour_mapping})
        df_non_band["Weight"] = df_non_band["Weight"].apply(float)
        df_band["Weight"] = df_band["Weight"].apply(float)
        return df_non_band, df_band

    def get_exercise_variation_df(self, exercise: str, variation: str) -> pd.DataFrame:
        exercises_non_band = self.df_non_band["Exercise"].unique()
        variations_non_band = self.df_non_band["Variation"].unique()

        exercises_band = self.df_band["Exercise"].unique()
        variations_band = self.df_band["Variation"].unique()

        if exercise in exercises_band and variation in variations_band:
            return self.df_band.loc[
                (self.df_band["Exercise"] == exercise)
                & (self.df_band["Variation"] == variation)
            ]
        if exercise in exercises_non_band and variation in variations_non_band:
            return self.df_non_band.loc[
                (self.df_non_band["Exercise"] == exercise)
                & (self.df_non_band["Variation"] == variation)
            ]

    def get_filled_df(self) -> pd.DataFrame:
        # remove rows with all nan values
        df = self.df_raw.dropna(how="all")
        # convert to upper case
        df = df.map(lambda x: x.upper() if isinstance(x, str) else x)
        # Remove trailing spaces from all string values
        df = df.map(lambda x: x.rstrip() if isinstance(x, str) else x)
        # fill 0 weight for selected Exercises
        # I was too lazy to fill in 0 when working out
        # <<Note>> This "Weight" column type is object b.c. the pre-filled values are strings.
        df.loc[(~df["Exercise"].isnull()) & (df["Weight"].isnull()), ["Weight"]] = 0
        # forward fill
        ffill_columns = ["Date", "Exercise", "Variation", "Weight"]
        [df[col].ffill(inplace=True) for col in ffill_columns]
        df.loc[df["Weight"]==0, "Weight"] = "1"

        # convert str to datetime
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        # count sets
        df["Set"] = df.groupby(["Date", "Exercise", "Variation"]).cumcount() + 1
        df.reset_index(drop=True, inplace=True)
        df["Set"] = df["Set"].apply(str)
        return df
