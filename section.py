import streamlit as st
from ui import severity_box
book_id = st.session_state.get("book_id", 1)
full_analysis = st.session_state.get(f"full_analysis_{book_id}")
if not full_analysis:
    st.warning("Upload a book first.")
    st.stop()

labels = list(sorted(full_analysis.keys()))
idx = min(max(st.session_state.get("section_idx",0), 0), len(labels) - 1)

col1, col2, col3 = st.columns([1, 4, 1])
if col1.button("◀ Previous", disabled= idx == 0):
    idx -= 1
if col3.button("Next ▶", disabled= idx == len(labels) - 1):
    idx += 1
st.session_state.section_idx = idx

first, last = labels[idx]
st.header(f"Pages {first} - {last}" if first != last else f"Pages {first}")
if full_analysis[labels[idx]] is None:
    st.warning("This section could not be analyzed. Try scanning the book again.")
    st.stop()
for item in full_analysis[labels[idx]]:
    st.subheader(item["genre"]+"\n")
    severity_box(item["analysis"], item['severity_score'])
    with st.expander(f"Quoted Instances of {item['genre']}"):
        for quote in item['quotes']:
            st.markdown("- "+f"\"{quote}\""+"\n")

