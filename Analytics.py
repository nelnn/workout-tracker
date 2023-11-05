import datetime
from pathlib import Path
import pandas as pd
import streamlit as st
import os

from src.body_weight import BodyWeight
from src.processing_raw import Processing
from src.plots import Plot
from src.get_data import get_data_from_gsheets, get_daily_workout

st.set_page_config(
    page_title="Gym Tracker",
    page_icon=":man-lifting-weights:"
)

PWD = os.path.dirname(os.path.abspath(__file__))
MD_DIR = os.path.join(PWD, "md/")


df_raw = get_data_from_gsheets()
df_bw = get_data_from_gsheets(sheet_name="Weight")
processing = Processing(df_raw=df_raw)
df_raw_filled = processing.get_filled_df()


@st.cache_data(ttl=600)
def read_markdown_file(markdown_file):
    dir = os.path.join(MD_DIR, markdown_file)
    return Path(dir).read_text()



# Custom Plots
container_custom = st.container()
with container_custom:
    st.subheader("Analytics")
    st.write("Display the total volume of an exercise. Volume is defined as either \
             weight*reps or *weight x seconds* depending on the specific exercise.")
    st.write("Select the exercise and variation to generate the plots.")
    col11, col12, col13 = st.columns(3)
    with col11:
        exercises = sorted(df_raw_filled["Exercise"].unique())
        default_exercise_option = exercises.index("BENCH PRESS")
        exercise_option = st.selectbox(
            "Exercise", tuple(exercises), index=default_exercise_option
        )
    with col12:
        variations = sorted(
            df_raw_filled[df_raw_filled["Exercise"] == exercise_option][
                "Variation"
            ].unique()
        )
        variations_option = st.selectbox("Variation", tuple(variations))
    with col13:
        date_range = [
            "Last 1 month",
            "Last 3 months",
            "Last 6 months",
            "Last 12 months",
        ]
        default_date_range_option = date_range.index("Last 3 months")
        date_range_option = st.selectbox(
            "Period", tuple(date_range), index=default_date_range_option
        )
    df = processing.get_exercise_variation_df(
        exercise=exercise_option, variation=variations_option
    )
    plots = Plot(df)

    tab1, tab2, tab3 = st.tabs(["Volume", "PR", "Additional Information"])

    with tab1:
        fig_volume = plots.volume_breakdown(date_range_option)
        st.plotly_chart(fig_volume, use_container_width=True)
    with tab2:
        fig_pr = plots.personal_record()
        st.plotly_chart(fig_pr, use_container_width=True)
    with tab3:
        plots_info_md = read_markdown_file("plot_details.md")
        st.markdown(plots_info_md, unsafe_allow_html=True)


container_bw = st.container()
with container_bw:
    st.subheader("Body Weight")
    bw = BodyWeight(df_bw)
    fig_bw = bw.body_weight_trend()
    st.plotly_chart(fig_bw, use_container_width=True)

container_df = st.container()
with container_df:
    st.subheader("Session")
    st.write(
        "Display the workout record of a given date. \
            Default shows the record of the latest session."
    )
    col21, col22 = st.columns([0.2, 0.8])
    with col21:
        input_date = st.date_input("Date", df_raw_filled["Date"].max())
        df_day = get_daily_workout(df_raw_filled, input_date)
    with col22:
        st.dataframe(df_day)
