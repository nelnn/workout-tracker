from pathlib import Path
import pandas as pd
import streamlit as st
import os

from src.body_weight import BodyWeight
from src.processing_raw import Processing
from src.plots import Plot
from src.get_data_from_gsheets import get_raw_data, load_data

import src.updated_timestamp

PWD = os.path.dirname(os.path.abspath(__file__))
MD_DIR = os.path.join(PWD, "md/")

# df_raw, df_bw = get_raw_data()

df_raw = load_data()
df_bw = load_data(sheet_name="Weight")

processing = Processing(df_raw=df_raw)

df_raw_filled = processing.get_filled_df()


@st.cache_data(ttl=600)
def read_markdown_file(markdown_file):
    dir = os.path.join(MD_DIR, markdown_file)
    return Path(dir).read_text()


intro_markdown = read_markdown_file("introduction.md")
st.markdown(intro_markdown, unsafe_allow_html=True)


st.subheader("Performance")
st.write("Select the exercise and variation to generate the plots.")

# Custom Plots
container_custom = st.container()
with container_custom:
    col11, col12 = st.columns(2)
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

    df = processing.get_exercise_variation_df(
        exercise=exercise_option, variation=variations_option
    )
    plots = Plot(df)

    tab1, tab2, tab3 = st.tabs(["Volume", "PR", "Additional Information"])

    with tab1:
        fig_volume = plots.volume_breakdown()
        st.plotly_chart(fig_volume, use_container_width=True)
    with tab2:
        fig_pr = plots.personal_record()
        st.plotly_chart(fig_pr, use_container_width=True)
    with tab3:
        plots_info_md = read_markdown_file("plot_details.md")
        st.markdown(plots_info_md, unsafe_allow_html=True)


container_bw = st.container()
with container_bw:
    # df_bw = pd.read_csv(WEIGHT_DIR, index_col=0)
    bw = BodyWeight(df_bw)
    fig_bw = bw.body_weight_trend()
    st.plotly_chart(fig_bw, use_container_width=True)
