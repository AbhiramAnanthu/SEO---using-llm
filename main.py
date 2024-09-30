from search import get_search_results
import streamlit as st

keyword = st.text_input(label="Search bar for movie", placeholder="interstellar")
results = get_search_results(keyword)
for re in results:
    st.write(re["title"])
