from fastapi import FastAPI, HTTPException, Response
from agent_bob.model.fetcher import get_user_data
from agent_bob.model.recommender import recommend_bottles
from agent_bob.model.embedder import load_bottles_data, initialize_vectorizers, create_embeddings, load_baxus_embeddings, embeddings_exist, BAXUS_EMBEDDINGS_PATH
from cachetools import TTLCache
from contextlib import asynccontextmanager
import numpy as np
from typing  import Optional

user_cache = TTLCache(maxsize=1000, ttl=300)  


@asynccontextmanager
async def lifespan(app:FastAPI):
    global baxus_embeddings
    
    baxus_data = load_bottles_data()
    initialize_vectorizers(baxus_data)

    if embeddings_exist():
        baxus_embeddings = load_baxus_embeddings()
    else:
        baxus_embeddings = create_embeddings(baxus_data)
        with open(BAXUS_EMBEDDINGS_PATH, "wb") as f:
            np.save(f, baxus_embeddings)
    
    app.state.baxus_embeddings = baxus_embeddings
    app.state.baxus_data = baxus_data

    yield

app = FastAPI(lifespan=lifespan)
    
@app.head("/")
def system_check():
    return Response(status_code=200)    

@app.get("/")
def server_test():
    return {"message": "Server is running"}

@app.get("/recommend/user/{username}")
async def get_recommendations(username: str, limit: Optional[int] = 3):

    if limit < 1 or limit > 10 :
        raise HTTPException(status_code=400, detail="Limit must be between 1 and 10")
    
    # Fetch user data from Baxus API
    user_data = get_user_data(username)
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    cache_key=f"{username}_{limit}"
    if cache_key in user_cache:
        return user_cache[cache_key]

    # Recommend bottles based on user data
    recommendations = recommend_bottles(user_data,app.state.baxus_embeddings,app.state.baxus_data,limit)
    user_cache[cache_key] = recommendations

    return recommendations
