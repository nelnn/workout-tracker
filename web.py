import pandas as pd
import streamlit as st
import os

from src.body_weight import BodyWeight
from src.processing_raw import Processing
from src.plots import Plot
from src.get_data_from_gsheets import get_raw_data

import src.updated_timestamp

df_raw, df_bw = get_raw_data()

processing = Processing(df_raw=df_raw)

df_raw_filled = processing.get_filled_df()
st.header("Gym Tracker")
st.write(
    "Hi! My name is Nelson. \
    This is my workout tracker where I record my progess in Weightlifting and Calisthenics!"
)

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
        st.write("**Resistance Band**")
        st.markdown(
            "- I use resistance bands for some Calisthenics exercises \
            and I have 4 bands of different thickness. Since I cannot quantify the strength of \
            the bands with definite values, I assign the lighest band 0.8kg, \
            second lightest 0.6kg, third 0.2kg, and the heaviest 0.1kg."
        )
        st.write("**Body Weight**")
        st.markdown(
            "- If no weight is added to the exercise we set the weight \
            to $1$ in order to plot the total volume."
        )
        st.write("**Count**")
        st.markdown(
            "- The 'Count' variable specifies the number of reps or\
                     the number of seconds performed for the exercise."
        )


container_bw = st.container()
with container_bw:
    # df_bw = pd.read_csv(WEIGHT_DIR, index_col=0)
    bw = BodyWeight(df_bw)
    fig_bw = bw.body_weight_trend()
    st.plotly_chart(fig_bw, use_container_width=True)
