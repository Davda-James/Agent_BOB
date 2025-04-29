import numpy as np
from .embedder import create_user_embeddings, compute_similarity, generate_recommendation_reason
import pandas as pd


# Function to recommend bottles
def recommend_bottles(user_data,baxus_embeddings,baxus_data,limit):
    # Load static 501 bottles data
    # all_bottles = load_bottles_data()
    
    # initialize_vectorizers(all_bottles)  

    # Create embeddings for all bottles
    # all_bottles_embeddings = create_embeddings(baxus_embeddings)
    

    # Get user’s bottles (those in their virtual bar)
    user_bottles = user_data
    
    # Create user’s bottle embeddings
    user_embeddings = create_user_embeddings(user_bottles)

    # Compute similarity between user’s bottles and all 501 bottles
    similarities = compute_similarity(user_embeddings,baxus_embeddings)

    recommended_bottles=[]

    for i in range(similarities.shape[0]):
        # Get similarity scores for this user bottle compared to all bottles
        bottle_similarities = similarities[i]
        
        similar_indices = np.argsort(-bottle_similarities)

        for j in range(min(limit, len(similar_indices))):  # Get top 5 recommendations
            index = int(similar_indices[j])  # Convert to integer scalar
            recommended_bottles.append(baxus_data[index])
    
    keys_to_keep = ['name', 'spirit_type',"popularity","avg_msrp","image_url","ranking","proof","abv","shelf_price"]
    sanitized_recommendations = []
    for bottle in recommended_bottles:
        sanitized_bottle = {}
        reason= generate_recommendation_reason(bottle, user_bottles)
        for key, value in bottle.items():
            # Check if value is NaN and replace with None or default value
            if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
                if key in ['name', 'spirit_type']:
                    sanitized_bottle[key] = "Unknown"
                else:
                    sanitized_bottle[key] = 0
            elif key in keys_to_keep:
                sanitized_bottle[key] = value
        sanitized_bottle["reason"]= reason
        sanitized_recommendations.append(sanitized_bottle)

    # Remove duplicates if any
    unique_recommendations = []
    seen_names = set()
    for bottle in sanitized_recommendations:
        name = bottle.get('name', '')
        if name not in seen_names:
            seen_names.add(name)
            unique_recommendations.append(bottle)
    
    # Return top unique recommendations (limit to 10)
    return unique_recommendations[:limit]
    # return {} 