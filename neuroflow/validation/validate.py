# validate.py
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
from importlib.resources import files

def get_icon_path():
    return str(files("neuroflow") / "validation" / "assets" / "neuroflow.ico")

def main(file_path):
    st.set_page_config(
        page_title="NeuroFlow Validator",
        # page_icon=get_icon_path(),
        layout="wide"
    )
    # CSS injection to hide Streamlit branding/footer/deploy button
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}  /* hamburger menu */
        footer {visibility: hidden;}     /* footer */
        header {visibility: hidden;}     /* "Deploy this app" button */
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    st.title("NeuroFlow Data Validator")

    df = pd.read_csv(file_path)

    st.write("### Data Preview")
    st.dataframe(df.head())

    # Pick columns to plot
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    selected_cols = st.multiselect("Columns", numeric_cols)

    if len(selected_cols) > 0:
        fig = px.line(df, y=selected_cols, color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate.py <file.csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
