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


def generate_embedding(collection_name: str, field_name: str):
    chroma_client = chromadb.Client()
    try:
        embedd_collections = chroma_client.get_collection(collection_name)
    except Exception as e:
        embedd_collections = chroma_client.create_collection(collection_name)

    documents = list(collection.find({field_name: {"$exists": True}}).limit(50))

    # Generate embeddings for the "plot" field
    embeddings = model.encode([doc[field_name] for doc in documents])

    # Generate unique IDs for each document
    ids = [f"id_{i}" for i in range(len(documents))]

    # Add each embedding to the Chroma collection with its corresponding ID
    for doc, embedding, doc_id in zip(documents, embeddings, ids):
        embedd_collections.add(
            embeddings=[
                embedding
            ],  # Wrap in a list since add() expects a list of embeddings
            ids=doc_id,  # Wrap in a list to match the embedding list
            metadatas=[
                {"_id": str(doc["_id"])}
            ],  # Optional: Store MongoDB _id as metadata
        )

    return embedd_collections


def search_embedding(text: str, collection_name: str) -> object:
    data = []
    query = model.encode(text)
    results = collection_name.query(query_embeddings=query)
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


