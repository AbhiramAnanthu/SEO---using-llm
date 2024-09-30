from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import chromadb
import os

# Load environment variables
load_dotenv(dotenv_path=".env")

# Initialize the model and MongoDB client
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = MongoClient(os.getenv("MONGODB"))
db = client.sample_mflix
collection = db.movies

# Initialize the Chroma client and create a collection for embeddings
chroma_client = chromadb.Client()
embedd_collection = chroma_client.create_collection("movie_search")

# Fetch documents with "plot" field
documents = list(collection.find({"plot": {"$exists": True}}).limit(50))

# Generate embeddings for the "plot" field
embeddings = model.encode([doc["plot"] for doc in documents])

# Generate unique IDs for each document
ids = [f"id_{i}" for i in range(len(documents))]

# Add each embedding to the Chroma collection with its corresponding ID
for doc, embedding, doc_id in zip(documents, embeddings, ids):
    embedd_collection.add(
        embeddings=[
            embedding
        ],  # Wrap in a list since add() expects a list of embeddings
        ids=doc_id,  # Wrap in a list to match the embedding list
        metadatas=[{"_id": str(doc["_id"])}],  # Optional: Store MongoDB _id as metadata
    )

# query = model.encode("")
# results = embedd_collection.query(query_embeddings=query)
# results_id = [id for id in results["metadatas"][0]]
# for id in results_id:
#     id_str = id["_id"]
#     document = collection.find_one({"_id": ObjectId(id_str)})
#     print(document["title"])


def get_search_results(text: str):
    data = []
    query = model.encode(text)
    results = embedd_collection.query(query_embeddings=query)
    results_id = [id for id in results["metadatas"][0]]
    for id in results_id:
        id_str = id["_id"]
        document = collection.find_one({"_id": ObjectId(id_str)})
        data.append(
            {
                "title": document["title"],
                "rating_imdb": document["imdb"]["rating"],
            }
        )
    return data

