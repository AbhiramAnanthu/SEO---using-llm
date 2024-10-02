from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import chromadb
import os

load_dotenv(dotenv_path=".env")

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = MongoClient(os.getenv("MONGODB"))
db = client.sample_mflix
collection = db.movies
chroma_client = chromadb.Client()


def generate_embedding(collection_name: str, field_name: str):
    embedd_collections = chroma_client.create_collection(collection_name)
    documents = list(collection.find({field_name: {"$exists": True}}).limit(50))

    embeddings = model.encode([doc[field_name] for doc in documents])

    ids = [f"id_{i}" for i in range(len(documents))]

    for doc, embedding, doc_id in zip(documents, embeddings, ids):
        embedd_collections.add(
            embeddings=[embedding],
            ids=doc_id,
            metadatas=[{"_id": str(doc["_id"])}],
        )

    return embedd_collections


def search_embedding(text: str, collection_name: str, field_name: str) -> object:
    data = []
    try:
        embedd_collection = chroma_client.get_collection(collection_name)
    except:
        embedd_collection = generate_embedding(collection_name, field_name)
    query = model.encode(text)
    results = embedd_collection.query(query_embeddings=query)
    results_id = [id for id in results["metadatas"][0]]
    for id in results_id:
        id_str = id["_id"]
        document = collection.find_one({"_id": ObjectId(id_str)})
        try:
            poster = document["poster"]  # Attempt to access the 'poster' key
            data.append(
                {
                    "title": document["title"],
                    "poster": poster,
                    "rating_imdb": document["imdb"]["rating"],
                }
            )
        except KeyError:  # Catch the KeyError if 'poster' doesn't exist
            data.append(
                {
                    "title": document["title"],
                    "rating_imdb": document["imdb"]["rating"],
                }
            )

    return data
