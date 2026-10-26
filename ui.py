import streamlit as st

CSS = """
<style>
[data-testid="stHeader"] {background: transparent;}
[data-testid="stMainBlockContainer"] {padding-top: 2.5rem; max-width: 1200px;}
h1, h2, h3 {letter-spacing: -0.01em;}

/* Hero banner */
.bcs-hero {background: linear-gradient(135deg, #5A4BD6 0%, #6C5CE7 45%, #A29BFE 100%);
  color: #fff; border-radius: 20px; padding: 2rem 2.25rem; margin-bottom: 1.5rem;
  box-shadow: 0 12px 30px -12px rgba(108, 92, 231, 0.55);}
.bcs-eyebrow {font-size: 0.75rem; font-weight: 600; letter-spacing: 0.14em; opacity: 0.85;}
.bcs-title {font-family: "Source Serif 4", serif; font-size: 2.4rem; font-weight: 700;
  line-height: 1.15; margin: 0.35rem 0 0.6rem;}
.bcs-sub {font-size: 1.02rem; max-width: 680px; opacity: 0.95; margin: 0;}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {background: #fff; border: 2px dashed #C9C3F3;
  border-radius: 16px; padding: 1.5rem; transition: border-color 0.15s, background 0.15s;}
[data-testid="stFileUploaderDropzone"]:hover {border-color: #6C5CE7; background: #F8F7FE;}

/* Buttons */
.stButton > button, .stDownloadButton > button {border-radius: 10px; font-weight: 600;
  padding: 0.45rem 1.1rem; transition: transform 0.12s, box-shadow 0.12s, border-color 0.12s;}
.stButton > button:hover, .stDownloadButton > button:hover {transform: translateY(-1px);
  border-color: #6C5CE7; box-shadow: 0 6px 16px -8px rgba(108, 92, 231, 0.6);}

/* Tabs */
[data-baseweb="tab-list"] {gap: 0.25rem; border-bottom: 1px solid #E4E2EE;}
[data-baseweb="tab"] {padding: 0.6rem 1.1rem; font-weight: 600; border-radius: 10px 10px 0 0;}
[data-baseweb="tab"][aria-selected="true"] {background: #F1F0F7;}

/* Cards around tables, charts, expanders and alerts */
[data-testid="stPlotlyChart"] {background: transparent !important;}
[data-testid="stDataFrame"], [data-testid="stPlotlyChart"] {box-sizing: border-box; max-width: 100%; background: #fff;
  border: 1px solid #E4E2EE; border-radius: 14px; padding: 0.5rem;
  box-shadow: 0 2px 10px -6px rgba(30, 30, 46, 0.15);}
[data-testid="stExpander"] details {background: #fff; border-radius: 12px; border-color: #E4E2EE;}
[data-testid="stExpander"] summary {font-weight: 600;}
[data-testid="stAlert"] {border-radius: 12px;}

/* Quotes inside expanders */
[data-testid="stExpander"] ul {padding-left: 0;}
[data-testid="stExpander"] li {list-style: none; margin: 0.45rem 0; padding: 0.55rem 0.9rem;
  background: #F6F5FC; border-left: 3px solid #6C5CE7; border-radius: 0 8px 8px 0;
  font-family: "Source Serif 4", serif; font-style: italic;}

/* Sidebar */
[data-testid="stSidebarNav"] a {border-radius: 8px;}

/* Typography: serif for page titles, small caps-style sans labels for genre headings */
h1, h2 {font-family: "Source Serif 4", serif !important; font-weight: 700 !important;}
[data-baseweb="tab"] p, [data-testid="stExpander"] summary p {font-weight: 600;}
h3 {font-family: "Inter", sans-serif !important; font-size: 0.95rem !important; font-weight: 700 !important;
  letter-spacing: 0.08em; text-transform: uppercase; color: #4B4870;
  margin-top: 1.4rem !important; padding-top: 1.1rem !important; border-top: 1px solid #E4E2EE;}
[data-testid="stWidgetLabel"] p {font-weight: 600; color: #3A3756;}
[data-testid="stCaptionContainer"], .stMarkdown p {line-height: 1.6;}

/* Section list (Overview tab): buttons keyed open_* become a wrapping grid of pills */
[data-testid="stVerticalBlock"]:has(> [class*="st-key-open_"]) {flex-direction: row; flex-wrap: wrap; gap: 0.6rem;}
[data-testid="stVerticalBlock"]:has(> [class*="st-key-open_"]) > :not([class*="st-key-open_"]) {flex: 1 1 100%; width: 100% !important;}
[class*="st-key-open_"] {flex: 0 0 auto; width: auto !important;}
[class*="st-key-open_"] button {background: #fff; border: 1px solid #E4E2EE; border-radius: 999px;
  padding: 0.4rem 1rem; font-weight: 600; color: #3A3756;}
[class*="st-key-open_"] button:hover {background: #F1F0F7; color: #5A4BD6;}

/* Max-score buttons (Table Display view), keyed max_*, styled as stat cards */
[class*="st-key-max_"] button {width: 100%; min-height: 96px; height: 100%;
  background: #fff; border: 1px solid #E4E2EE; border-top: 4px solid #6C5CE7; border-radius: 14px;
  box-shadow: 0 2px 10px -6px rgba(30, 30, 46, 0.18); white-space: normal; line-height: 1.35;
  padding: 0.6rem 0.45rem;}
[class*="st-key-max_"] button div,
[class*="st-key-max_"] button p {font-size: 0.82rem; font-weight: 600; color: #3A3756;
  white-space: normal; overflow: visible; text-overflow: clip; max-width: 100%; text-align: center;
  word-break: normal; overflow-wrap: normal; hyphens: none;}
[class*="st-key-max_"] button:hover {border-top-color: #5A4BD6; background: #FBFAFF;}
[class*="st-key-max_"], [class*="st-key-max_"] .stButton {height: 100%; width: 100% !important;}
/* Let the five cards wrap onto a second row when the window is too narrow for their labels */
[data-testid="stHorizontalBlock"]:has([class*="st-key-max_"]) {display: grid !important;
  grid-template-columns: repeat(auto-fit, minmax(145px, 1fr)); gap: 1rem; margin-bottom: 1rem;}
[data-testid="stHorizontalBlock"]:has([class*="st-key-max_"]) > [data-testid="stColumn"] {
  width: auto !important; min-width: 0 !important;}
/* Genre color on each card, matching the chart colors */
[class*="st-key-max_Romantic"] button {border-top-color: #E84393;}
[class*="st-key-max_Dark"] button {border-top-color: #475569;}
[class*="st-key-max_Violence"] button {border-top-color: #D63031;}
[class*="st-key-max_Alcohol"] button {border-top-color: #E1A200;}

/* "Go to Section Details" buttons under the charts read as the primary action */
.st-key-all button, .st-key-individual button {background: #6C5CE7; color: #fff; border-color: #6C5CE7;}
.st-key-all button:hover, .st-key-individual button:hover {background: #5A4BD6; color: #fff;}

/* Rubric page */
.st-key-rubric {background: #fff; padding: 0.5rem 1rem;}
.st-key-rubric h1 {font-size: 1.6rem !important;}
.st-key-rubric h2 {font-family: "Inter", sans-serif !important; font-size: 1rem !important;
  letter-spacing: 0.08em; text-transform: uppercase; color: #5A4BD6; margin-top: 1.5rem !important;
  padding-top: 1.1rem; border-top: 1px solid #E4E2EE;}
.st-key-rubric hr {display: none;}
</style>
"""

def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)

def hero():
    st.markdown(
        '<div class="bcs-hero">'
        '<div class="bcs-eyebrow">CONTENT ADVISORY</div>'
        '<div class="bcs-title">ReadAhead</div>'
        '<p class="bcs-sub">Upload a book and get a section-by-section breakdown of its content, '
        'each of 5 genres scored against a consistent rubric.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

def severity_color(score):
    if score <= 3:
        return "green"
    if score <= 6:
        return "orange"
    return "red"

def severity_box(text, score):
    box = {"green": st.success, "orange": st.warning, "red": st.error}[severity_color(score)]
    box(f"{text}\n\n**Severity: {score}/10**")
