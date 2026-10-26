import streamlit as st

with open("rubric.txt") as rubric_file:
    rubric=rubric_file.read()

st.title("How was your text scored?")

st.info('''Below is the rubric that the API is prompted to score each section of text on.''')

with st.container(border=True, key="rubric"):
    st.markdown(rubric)