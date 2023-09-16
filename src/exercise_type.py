import pandas as pd


def pick_df(df: pd.DataFrame, exercise: str, variation: str) -> pd.DataFrame:
    """
    This function is used to separate exercises with and without assistance bands,
    since the "Weights" for bands are not floats and need to be converted to
    some numerical representation.
    -----------
    Parameters:
    -----------
    df: The original pd.DataFrame downloaded from the server
    exercise: Exercise to be ploted
    variation: Variation to be plotted
    --------
    Returns:
    --------
    pd.DataFrame

    """
    # convert date to datetime
    df["Date"] = pd.to_datetime(df["Date"])
    # select exercises with assistant bands
    assistant_band_exercises = df["Weight"].str.isalpha()
    assistant_band_exercises = df[assistant_band_exercises]["Exercise"].unique()
    df_band = df[df["Exercise"].isin(assistant_band_exercises)]
    exercises_band = df_band["Exercise"].unique()
    variations_band = df_band["Variation"].unique()

    df_non_band = df[~df["Exercise"].isin(exercises_band)]

    exercises_non_band = df_non_band["Exercise"].unique()
    variations_non_band = df_non_band["Variation"].unique()

    # purple, black, green, orange
    band_colour_mapping = {"P": -10, "B": -20, "G": -30, "O": -40}
    df_band = df_band.replace({"Weight": band_colour_mapping})

    # convert object to float
    df_band["Weight"] = pd.to_numeric(df_band["Weight"])
    df_non_band["Weight"] = pd.to_numeric(df_non_band["Weight"])

    if exercise in exercises_band and variation in variations_band:
        return df_band.loc[
            (df_band["Exercise"] == exercise) & (df_band["Variation"] == variation)
        ]
    if exercise in exercises_non_band and variation in variations_non_band:
        return df_non_band.loc[
            (df_non_band["Exercise"] == exercise)
            & (df_non_band["Variation"] == variation)
        ]
    return "Invalid Request"
