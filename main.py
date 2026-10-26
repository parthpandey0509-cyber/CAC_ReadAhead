from intake import convert_read
import streamlit as st
from scanner import analysis
import concurrent.futures
import time
import hashlib
import sqlite3
import json
import pandas as pd
import plotly.express as px
from llm import title_request
from ui import hero
conn=sqlite3.connect("BookScanner.db")
cursor=conn.cursor()
cursor.execute(f"CREATE TABLE IF NOT EXISTS books(identifier TEXT PRIMARY KEY, Title TEXT, Saved TEXT, analysis TEXT)")
genres=["PROFANITY", "ROMANTIC/EXPLICIT CONTENT", "DARK/HEAVY THEMES", "VIOLENCE/SCARINESS", 
                    "ALCOHOL/SUBSTANCE USE"]
def display(genres, book_id):
    view=st.segmented_control("View",["Overview", "Table Display", "Content Map", "Genre Maps"], default="Overview", key="view", required=True)
    full_analysis=st.session_state[f'full_analysis_{book_id}']
    if all(section is None for section in full_analysis.values()):
        st.error("Analysis failed for every section. Is Ollama running?")
        return
    genre_scores={"Profanity": [], "Romantic/Explicit Content":[], "Dark/Heavy Themes":[], "Violence/Scariness":[],"Alcohol/Substance Use":[]}
    for label, analyzed in sorted(full_analysis.items()):
        scores = {item["genre"]: item["severity_score"] for item in analyzed} if analyzed else {}
        for genre in genre_scores.keys():
            genre_scores[genre].append(scores.get(genre.upper()))
    if view =="Overview":
        severity_search=st.slider("Filter by Severity", 1, 10)
        genre_search=st.multiselect("Filter by Genre: ",
        genres, default=genres[0])
        sect_idx=0
        for label, analyzed in sorted(full_analysis.items()):
            if analyzed is None:
                sect_idx+=1
                continue
            scores = {item["genre"]: item["severity_score"] for item in analyzed}
            if any([scores.get(g_s, 0) >= severity_search for g_s in genre_search]):
                button_label=""
                if label[0]==label[1]:
                    button_label=f"{label[0]}"
                else:
                    button_label=f"{label[0]} - {label[1]}"
                if st.button(f"Pages {button_label}", key=f"open_{label}"):
                    st.session_state.section_idx = sect_idx
                    st.switch_page("section.py")
            sect_idx+=1
    if view=="Table Display":
        st.write("Go right to the where the highest severity scores were detected: ")
        col1, col2, col3, col4, col5=st.columns(5)
        cols=[col1, col2, col3, col4, col5]
        g_s_keys=list(genre_scores.keys())
        for col,genre in zip(cols,g_s_keys):
            with col:
                peak=max(score for score in genre_scores[genre] if score is not None)
                if st.button(f"Max {genre} Score: {peak}/10", key=f"max_{genre}"):
                    st.session_state.section_idx=genre_scores[genre].index(peak)
                    st.switch_page("section.py")


        rows = [({"Section": f"Pages {(str(label[0])+" - "+str(label[1])) if label[0]!=label[1] else str(label[0])}", **{i["genre"]:i["severity_score"] for i in items } }) for label, items in sorted(full_analysis.items()) if items]

        df=pd.DataFrame(rows).set_index("Section")
        st.dataframe(df, column_config={genre: st.column_config.ProgressColumn(min_value=0,max_value=10, format="%d") for genre in genres})
    if view=="Content Map":   
        df_scores=pd.DataFrame(genre_scores)
        df_scores.index=df_scores.index+1
        fig_all=px.line(
            df_scores, 
            x=df_scores.index,
            y=df_scores.columns,
            markers=True,
            range_x=[1,len(df_scores)],
            range_y=[1,10],
            labels={
                "x":"Sections of 5 pages across the book",
                "value": "Severity Scores",
                "variable":"Genre"
            }
        )
        step=max(1, len(df_scores) //10)
        fig_all.update_xaxes(tick0=1, dtick=step)
        selected=st.plotly_chart(fig_all, on_select="rerun", selection_mode="points", key="main_chart")
        if selected and "selection" in selected and selected["selection"]["points"]!=[]:    
                    val=round(selected["selection"]["points"][0]["x"])
                    st.success(f"Selected Section: {val}")
                    if st.button("Go to Section Details", key="all"):
                        st.session_state.section_idx = val-1
                        st.switch_page("section.py")
    if view =="Genre Maps":    
        df_scores=pd.DataFrame(genre_scores)
        df_scores.index=df_scores.index+1
        step=max(1, len(df_scores) //10)
        option=st.selectbox(f"View a genre individually", genre_scores.keys(), key="individual_genre")
        fig=px.line(
            df_scores, 
            x=df_scores[option].index,
            y=[option],
            markers=True,
            range_x=[1,len(df_scores)],
            range_y=[1,10],
            labels={
                "x":"Sections of 5 pages across the book",
                "value": f"Severity Scores for {option}",
                "variable":"Genre"
            }
        )
        fig.update_xaxes(tick0=1, dtick=step)
        selected_small=st.plotly_chart(fig, on_select="rerun", selection_mode="points", key="genre_chart")
        if selected_small and ("selection" in selected_small) and (selected_small["selection"]["points"]!=[]):    
            val=round(selected_small["selection"]["points"][0]["x"])
            st.success(f"Selected Section: {val}")
            if st.button("Go to Section Details", key="individual"):
                st.session_state.section_idx = val-1
                st.switch_page("section.py")
    if st.button("View other saved texts"):
        st.switch_page("database.py")
    if st.button("View the rubric"):
        st.switch_page("rubric.py")
    
    
hero()
uploaded_file=st.file_uploader("Upload your text here:", type=["pdf", "epub", "mobi", "fb2", "xps", "txt"])
if "book_id" not in st.session_state:  
    st.session_state.book_id=0

with open("rubric.txt") as rubric_file:
    rubric=rubric_file.read()
if uploaded_file:
    book_id=hashlib.md5(uploaded_file.getvalue()).hexdigest()
    st.session_state.book_id=book_id
    if f"full_analysis_{book_id}" not in st.session_state:
        database_extraction=True
        entry=cursor.execute("SELECT identifier FROM books WHERE identifier=?", (book_id,)).fetchone()
        if entry is not None:
            try:    
                f_a_jsn=cursor.execute("SELECT analysis FROM books WHERE identifier=?", (book_id,)).fetchone()[0]
                f_a=json.loads(f_a_jsn)
                f_a_final={(int(key[:key.index(" ")]), int(key[key.index(" ")+1:])):value for key,value in f_a.items()}
                st.session_state[f"full_analysis_{book_id}"]=f_a_final
            except Exception as e:
                st.warning(f"Failed to retrieve text analysis from database, rerunning analysis: {e}")
                database_extraction=False
        if entry is None or database_extraction==False:    
            book_text=convert_read(uploaded_file)
            if not any(page.strip() for page in book_text):
                st.error("No readable text found. This file may be a scanned image without a text layer.")
                st.stop()
            full_analysis={}
            text=[" ".join(book_text[p:p+5]) for p in range(0,len(book_text),5)]
            results=[None]*len(text)
            progress_text="Analyzing your text..."
            progress=st.progress(0,text=progress_text)
            done=0
            with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
                future_to_idx={executor.submit(analysis, chunk,rubric):c for c,chunk  in enumerate(text)}
                for future in concurrent.futures.as_completed(future_to_idx):
                    i=future_to_idx[future]
                    results[i]=future.result()
                    first=(i*5)+1
                    second=min((i*5)+5,len(book_text))
                    full_analysis[(first,second)]=results[i]
                    done+=1
                    progress.progress(done/len(text), text=progress_text)
                time.sleep(1)
                progress.empty()
                st.session_state[f'full_analysis_{book_id}']=full_analysis
                full_analysis_jsn={f"{key[0]} {key[1]}":value for key,value in full_analysis.items()}
                title_prompt='''Generate a title for the given text. Output ONLY the title, with zero
                prose(such as, 'Here is your title, ' or anything like that) or extra characters before or after the output.'''
                try:
                    title=title_request(1, title_prompt, " ".join(book_text[:5]))
                except Exception:
                    title="Untitled"
                if None not in results: 
                    cursor.execute(f"INSERT OR REPLACE INTO books VALUES(?,?,?,?)", (str(book_id), title, str(time.ctime()),json.dumps(full_analysis_jsn)))
                    conn.commit()
    display(genres, book_id)
elif f"full_analysis_{st.session_state.book_id}" in st.session_state:
    display(genres,st.session_state.book_id)

        


