from search import search_embedding
import streamlit as st
import requests
from PIL import Image
from io import BytesIO


def image_handler(uri: str):
    try:
        response = requests.get(uri)
        if not response:
            print("invalid request url")
        image = Image.open(BytesIO(response.content))
        st.image(image, use_column_width=True,width=32)
    except Exception as e:
        st.error(e)


st.title("Movie Search Engine")

search_query = st.text_input("Search for movies", "")

results = search_embedding(search_query, "title_embedding", "title")
for res in results:
    st.write(f"{res['title']}\t\t{res['rating_imdb']}")
    try:
        poster_uri = res['poster']
        image_handler(poster_uri)
    except KeyError as e:
        st.write("poster not available")
