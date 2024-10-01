from search import get_search_results
import streamlit as st

st.title("Movie Search Engine")

    # Search bar
search_query = st.text_input("Search for movies", "")

    # Filters
with st.expander("Filters"):
    selected_genre = st.selectbox("Select Genre", ["", "Sci-Fi", "Thriller", "Romantic"])
    selected_language = st.selectbox("Select Language", ["", "English", "Korean", "French"])

    # Convert filters to a dictionary
filters = {
    "genre": selected_genre,
    "language": selected_language,
}

    # Search button
# if st.button("Search"):
#     if search_query:
#             # Perform search
#         # search_results = search_movies(search_query, filters)
#         if search_results:
#             st.write(f"Found {len(search_results)} result(s):")
#             for result in search_results:
#                 st.write(f"**Title**: {result['title']}")
#                 st.write(f"**Plot**: {result['plot']}")
#                 st.write(f"**Language**: {result['language']}")
#                 st.write(f"**Genre**: {result['genre']}")
#                 st.write("---")
#             else:
#                 st.write("No results found.")
#         else:
#             st.write("Please enter a search query.")
