from pathlib import Path
import os
import streamlit as st

PWD = os.path.dirname(os.path.abspath(__file__))
PARENT = Path(PWD).parent.absolute()
MD_DIR = os.path.join(PARENT, "md/")


@st.cache_data(ttl=600)
def read_markdown_file(markdown_file):
    dir = os.path.join(MD_DIR, markdown_file)
    return Path(dir).read_text()


logs_markdown = read_markdown_file("dairy.md")
st.markdown(logs_markdown, unsafe_allow_html=True)