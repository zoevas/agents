import numpy as np
from sentence_transformers import SentenceTransformer

encoder = SentenceTransformer("all-MiniLM-L6-v2")

hotels_database = [
    {
        "name": "City Center Hotel",
        "description": "mid budget hotel near the city center with breakfast and wifi",
        "price": 120,
    },
    {
        "name": "Luxury Grand Hotel",
        "description": "high budget luxury hotel with spa, pool, restaurant, and premium rooms",
        "price": 300,
    },
    {
        "name": "Budget Stay Inn",
        "description": "low budget simple hotel with basic rooms and affordable prices",
        "price": 60,
    },
]

hotel_embeddings = encoder.encode(
    [hotel["description"] for hotel in hotels_database],
    convert_to_numpy=True,
)


def normalize_preferences(preferences) -> str:
    if isinstance(preferences, dict):
        return " ".join(f"{key}: {value}" for key, value in preferences.items())

    if isinstance(preferences, list):
        return " ".join(str(item) for item in preferences)

    return str(preferences)


def get_target_price(preferences_text: str) -> int:
    preferences_text = preferences_text.lower()

    if "low" in preferences_text or "budget" in preferences_text:
        return 80

    if "high" in preferences_text or "luxury" in preferences_text:
        return 300

    return 150


def calculate_price_score(price: float, target_price: float) -> float:
    difference = abs(price - target_price)

    # Score between 0 and 1
    score = max(0, 1 - (difference / target_price))

    return score


def search_hotels(preferences, top_k: int = 3):
    preferences_text = normalize_preferences(preferences)

    pref_embedding = encoder.encode(
        [preferences_text],
        convert_to_numpy=True,
    )[0]

    # Semantic similarity
    similarity_scores = np.dot(hotel_embeddings, pref_embedding)

    # Normalize similarity to 0-1
    similarity_scores = (
        similarity_scores - similarity_scores.min()
    ) / (similarity_scores.max() - similarity_scores.min() + 1e-8)

    target_price = get_target_price(preferences_text)

    ranked_hotels = []

    for hotel, similarity in zip(hotels_database, similarity_scores):
        price_score = calculate_price_score(
            hotel["price"],
            target_price,
        )

        final_score = (similarity * 0.7) + (price_score * 0.3)

        ranked_hotels.append({
            **hotel,
            "similarity_score": round(float(similarity), 3),
            "price_score": round(float(price_score), 3),
            "final_score": round(float(final_score), 3),
        })

    ranked_hotels = sorted(
        ranked_hotels,
        key=lambda hotel: hotel["final_score"],
        reverse=True,
    )

    return ranked_hotels[:top_k]