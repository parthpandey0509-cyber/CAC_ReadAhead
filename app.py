import streamlit as st
from ui import inject_css
st.set_page_config(page_title="Book Content Scanner", page_icon=":material/menu_book:", layout="wide")
inject_css()

pages=[
    st.Page("main.py", title="Analysis", icon=":material/analytics:", default=True),
    st.Page("section.py", title="Details", icon=":material/article:"),
    st.Page("database.py", title="Saved Texts", icon=":material/bookmarks:"),
    st.Page("rubric.py", title="Analysis Rubric", icon=":material/rubric:")
]
st.navigation(pages).run()