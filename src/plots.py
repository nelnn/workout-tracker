import ipywidgets as widgets
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

from exercise_type import pick_df


class Plot:
    def __init__(self, df: pd.DataFrame):
        """
        This class contains a range of performance metrics visualised using plotly.
        """
        self.df = df
        self.exercise = self.df["Exercise"].values[0]
        self.variation = self.df["Variation"].values[0]

    # def _get_exercise_variation_df(self):
    #     return self.df.loc[
    #         (self.df["Exercise"] == self.exercise)
    #         & (self.df["Variation"] == self.variation)
    #     ]

    def personal_record(self) -> None:
        """
        Plot the Personal Record (PR) of a given exercise and variation across time.
        """
        pr = -np.inf
        date_arr = []
        weight_arr = []
        counts_arr = []

        for date in self.df["Date"]:
            temp = self.df.loc[self.df["Date"] == date]
            max_weight = temp["Weight"].max()

            max_weight_str = temp["Weight"].max()
            counts = temp.loc[temp["Weight"] == max_weight_str]["Count"].max()
            if max_weight > pr:
                pr = max_weight
                date_arr.append(date)
                weight_arr.append(max_weight)
                counts_arr.append(counts)

        variation = "" if self.variation == "/" else self.variation

        fig = go.Figure(
            [
                go.Scatter(
                    x=date_arr,
                    y=weight_arr,
                    marker=dict(
                        size=counts_arr,
                        sizemode="area",
                        sizeref=2.0 * max(counts_arr) / (40.0**2),
                        sizemin=4,
                    ),
                )
            ]
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="kg",
            title=f"{self.exercise} {variation} PR",
        )
        # <extra></extra> removes the "trace 0" text
        hovertemplate = (
            "Date: %{x}<br>"
            + "Weight: %{y} kg<br>"
            + "Count: %{customdata[0]}"
            + "<extra></extra>"
        )
        fig.update_traces(
            customdata=pd.DataFrame(counts_arr), hovertemplate=hovertemplate
        )
        fig.show()

    def volume(self) -> None:
        """
        Plot the total volume of the exercise across time.
        """

        df_groupby_date = (
            self.df.assign(col=self.df.Weight * self.df.Count)
            .groupby("Date", as_index=False)
            .col.sum()
        )

        fig = go.Figure(
            [
                go.Scatter(
                    x=df_groupby_date.Date,
                    y=df_groupby_date.col,
                )
            ]
        )

        variation = "" if self.variation == "/" else self.variation
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="kg",
            title=f"{self.exercise} {variation} PR",
        )
        fig.show()

    def volume_breakdown(self) -> None:
        df_groupby_date = (
            self.df.assign(col=self.df.Weight * self.df.Count)
            .groupby("Date", as_index=False)
            .col.sum()
        )
        fig = px.bar(self.df, x="Date", y="Weight", custom_data=["Count"], color="Set")
        hovertemplate = (
            "Date: %{x}<br>"
            + "Weight: %{y} kg<br>"
            + "Count: %{customdata[0]}"
            + "<extra></extra>"
        )

        fig.update_traces(hovertemplate=hovertemplate)
        fig.show()
