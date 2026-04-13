import numpy as np
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("all-MiniLM-L6-v2")

hotels_database = [
    {"name": "Grand Hotel", "description": "Luxury hotel in city center with spa.", "price": 300},
    {"name": "Boutique Resort", "description": "Cozy boutique hotel with top amenities.", "price": 250},
    {"name": "City View Hotel", "description": "Modern hotel with stunning city views.", "price": 200}
]

# Precompute embeddings once
hotel_embeddings = encoder.encode([h["description"] for h in hotels_database])

def search_hotels(preferences: str, top_k: int = 3):
    pref_embedding = encoder.encode(preferences)

    scores = np.dot(hotel_embeddings, pref_embedding)

    top_idx = scores.argsort()[-top_k:][::-1]

    return [{**hotels_database[i], "score": float(scores[i])} for i in top_idx]