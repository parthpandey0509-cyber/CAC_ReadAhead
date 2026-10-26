from llm import api_request
import streamlit as st
import json

def analysis(text, rubric, attempts=3):
    GENRES=["PROFANITY", "ROMANTIC/EXPLICIT CONTENT", "DARK/HEAVY THEMES", "VIOLENCE/SCARINESS", 
                    "ALCOHOL/SUBSTANCE USE"]
    prompt=f'''You are scanning a text for PROFANITY(specify all profane words used and censor as necessary), 
    ROMANTIC/EXPLICIT CONTENT, DARK/HEAVY THEMES, VIOLENCE/SCARINESS, and ALCOHOL/SUBSTANCE USE. You 
    will return a JSON object with a results key containing a list of exactly 5 objects, one for each genre given. NO EXTRA 
    PROSE OR TEXT SHOULD BE PRINTED, as this prompt is to be directly read with json.loads. Each dictionary 
    is formatted as "genre": "PLACEHOLDER" ,"analysis": "PLACEHOLDER", "quotes" : ["PLACEHOLDER", "PLACEHOLDER"], "severity_score": integer, with genre being a 
    string copied from the list, PROFANITY, ROMANTIC/EXPLICIT CONTENT,  DARK/HEAVY THEMES, VIOLENCE/SCARINESS, 
    ALCOHOL/SUBSTANCE USE. The analysis will contain a concise analysis summary of the text IN TERMS OF 
    THAT GENRE. The quotes will be a python list of the 2-3 of the most significant or telling quotes/phrases for 
    this genre of inappropriate content(if there is any such content) as strings(do not wrap the string quotes 
    in actual escape sequence quotes). Ensure that the quotes cover the most extreme parts of the text for that 
    genre that best represent your score. The severity score will be the evaluation of this content, based on 
    the specific genre, numerically based on the rubric provided in the system prompt. Use only the genres 
    corresponding section of this rubric for each genre. ALL STRINGS MUST BE ENCLOSED IN DOUBLE QUOTES. 
    YOUR RESPONSE SHOULD HAVE ZERO PROSE OR EXTRA EXPLANATION.'''

    for _ in range(attempts):
        try:
            response=api_request(1,prompt,text, rubric)
            data=json.loads(response)["results"]
            if sorted(d["genre"] for d in data) == sorted(GENRES) and len(data)==5 and all(1<=d["severity_score"]<=10 for d in data):
                return data
        except Exception as e:
            print(f"Retrying section: {e}")
    return None
    