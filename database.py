import streamlit as st
import sqlite3
import pandas as pd
import json
conn=sqlite3.connect("BookScanner.db")
cursor=conn.cursor()
df_identifier=pd.read_sql_query("SELECT identifier, Title, Saved FROM books", conn)
df=pd.read_sql_query("SELECT Title, Saved FROM books", conn)
st.title("Access Previously Scanned Texts Here")
row=st.dataframe(df, on_select="rerun", selection_mode="single-row")
if row and "selection" in row and row["selection"]["rows"]!=[]:
    index=row["selection"]["rows"][0]
    book_id=df_identifier['identifier'].iloc[index]
    full_analysis=json.loads(cursor.execute("SELECT analysis FROM books WHERE identifier=?", (book_id,)).fetchone()[0])
    full_analysis_final={(int(key[:key.index(" ")]), int(key[key.index(" ")+1:])):value for key,value in full_analysis.items()}
    st.session_state.book_id=book_id
    st.session_state[f"full_analysis_{book_id}"]=full_analysis_final
    st.switch_page("main.py")