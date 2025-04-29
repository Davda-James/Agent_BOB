from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import os
import pandas as pd

tfidf_vectorizer= TfidfVectorizer(max_features=100)
onehotencder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

BAXUS_EMBEDDINGS_PATH = os.path.join(os.path.dirname(__file__),"../data/baxus_embeddings.npy")
BAXUS_CSV_PATH = os.path.join(os.path.dirname(__file__),"../data/baxus_data.csv")



# Load static dataset of 501 bottles (this would be a JSON or CSV file)
def load_bottles_data():
    bottles_df = pd.read_csv(BAXUS_CSV_PATH)
    
    # Convert the DataFrame to a list of dictionaries, if needed
    bottles_data = bottles_df.to_dict(orient='records')

    return bottles_data


def normalize_proof(proof, min_proof=40, max_proof=150):
    if proof is None:
        return 0
    return (proof - min_proof) / (max_proof - min_proof)

def normalize_popularity(popularity, max_popularity=10000):
    if popularity is None or popularity <= 0:
        return 0
    return np.log1p(popularity) / np.log1p(max_popularity)

def normalize_price(price, min_price=10, max_price=5000):
    if price is None:
        return 0
    return (price - min_price) / (max_price - min_price)

def normalize_total_score(score, min_score=0, max_score=100):
    if score is None:
        return 0
    return (score - min_score) / (max_score - min_score)


def initialize_vectorizers(baxus_products):
    # Extract all names and spirit types from Baxus dataset
    names = [p.get('name', '') for p in baxus_products]
    spirit_types = [[p.get('spirit_type', 'Unknown')] for p in baxus_products]
    
    # Fit vectorizers on the FULL dataset
    tfidf_vectorizer.fit(names)
    onehotencder.fit(spirit_types)

def process_name(name):
    if name is None:
        name = ''
    name_vector =  tfidf_vectorizer.transform([name]).toarray()[0]
    return name_vector


def process_spirit_type(spirit_type):
    if spirit_type is None or not isinstance(spirit_type, str):
        spirit_type = 'Unknown'
    spirit_vector = onehotencder.transform([[spirit_type]])[0]
    return spirit_vector    


def create_feature_vector(p):
    numeric_features = [
        normalize_proof(p.get('proof')),
        normalize_popularity(p.get('popularity')),
        normalize_price(p.get('avg_msrp')),
        normalize_price(p.get('fair_price')),
        normalize_total_score(p.get('total_score'))
    ]
    name_features = process_name(p.get('name'))
    spirit_features = process_spirit_type(p.get('spirit_type'))
    
    full_feature = np.concatenate([name_features, spirit_features,numeric_features])
    return full_feature


# A basic TF-IDF vectorizer for generating bottle profile embeddings
def create_embeddings(products):
    bottles_features= [ create_feature_vector(p) for p in products ] 
    return np.array(bottles_features)   

def create_user_embeddings(user_bottles):
    # Convert user data to the right format
    user_products = extract_user_products(user_bottles)
    
    # Create embeddings using the SAME pre-trained vectorizers
    # (No fitting here, just transforming)
    user_features = [create_feature_vector(p) for p in user_products]
    return np.array(user_features)


def extract_user_products(user_bar_data):
    user_products = []
    for entry in user_bar_data:
        p = entry["product"]
        product = {
            'name': p['name'],
            'spirit_type': p['spirit'],   # your model expects 'spirit_type'
            'proof': float(p['proof']) if p['proof'] else 0,  # handle missing proof
            'popularity': float(p.get('popularity', 0)),  # handle missing popularity
            'avg_msrp': float(p.get('average_msrp', 0)),  # handle missing msrp
            'fair_price': float(p.get('fair_price', 0)),  # handle missing fair_price
            'total_score': 0,   # Placeholder if missing
        }
        user_products.append(product)
    return user_products

    


# Function to compute similarity
def compute_similarity(embeddings1,embeddings2):
    # Example: Replace NaN with the mean of each feature column
    embeddings1 = embeddings1.astype(np.float32)
    embeddings2 = embeddings2.astype(np.float32)

    embeddings1 = np.where(np.isnan(embeddings1), np.nanmean(embeddings1, axis=0), embeddings1)
    embeddings2 = np.where(np.isnan(embeddings2), np.nanmean(embeddings2, axis=0), embeddings2)

    cosine_similarities = cosine_similarity(embeddings1, embeddings2)
    return cosine_similarities



def embeddings_exist():
    if os.path.exists(BAXUS_EMBEDDINGS_PATH):
        return True
    return False

def load_baxus_embeddings():
    with open(BAXUS_EMBEDDINGS_PATH, "rb") as f:
        embeddings = np.load(f)
    return embeddings

def generate_recommendation_reason(recommeded_bottle, user_product):
    reasons = []

    # Match on spirit type
    preferred_spirits = {b['product']['spirit'] for b in user_product}
    if recommeded_bottle['spirit_type'] in preferred_spirits:
        reasons.append(f"Similar spirit type: {recommeded_bottle['spirit_type']}")

    # Price proximity
    user_prices = [b['product']['average_msrp'] for b in user_product if b['product']['average_msrp']]
    if user_prices:
        avg_price = sum(user_prices) / len(user_prices)
        if abs(recommeded_bottle['avg_msrp'] - avg_price) < 10:
            reasons.append(f"Close to your average price (${round(avg_price, 2)})")

    # ABV or proof similarity
    user_proof = [b['product']['proof'] for b in user_product if b['product']['proof']]
    if user_proof:
        avg_abv = sum(user_proof) / len(user_proof)
        if abs(recommeded_bottle['abv'] - avg_abv) <= 5:
            reasons.append(f"Similar proof: {recommeded_bottle['proof']}%")

    # Popularity
    if recommeded_bottle['popularity'] > 50000:
        reasons.append("Popular among users")

    # High score
    if recommeded_bottle['total_score'] > 800:
        reasons.append("Highly rated")

    return " | ".join(reasons) if reasons else "Recommended based on your taste profile"

