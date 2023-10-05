import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



class BodyWeight:
    """
    This class plots body weights related metrics.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.df["Date"] = pd.to_datetime(
            self.df["Date"], dayfirst=True, errors="coerce"
        )

    def body_weight_trend(self) -> px.line:
        fig = px.line(self.df, x="Date", y="kg")
        fig.update_traces(mode="markers+lines", hovertemplate=None, line_color="#39e6ba")
        fig.update_layout(hovermode="x unified")
        # fig.update_xaxes(range=[self.df["Date"][0], self.df["Date"][5]])
        fig.update_layout(dragmode='pan')
        return fig
