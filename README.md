<h1 align="center"> AGENT BOB </h1>
<div align="center">
  <img src="https://res.cloudinary.com/dgvnuwspr/image/upload/v1740441389/wdqjosbtpgjiyi1ovups.png">
</div>

![requests](https://img.shields.io/badge/requests-2.32.3-blue)
![uvicorn](https://img.shields.io/badge/uvicorn-0.34.2-blue)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.6.1-blue)
![cachetools](https://img.shields.io/badge/cachetools-5.5.2-blue)
[![Python](https://img.shields.io/pypi/pyversions/tensorflow.svg)](https://badge.fury.io/py/tensorflow)
[![FastAPI](https://img.shields.io/pypi/v/fastapi?color=green&label=FastAPI)](https://pypi.org/project/fastapi/)
[![NumPy](https://img.shields.io/pypi/v/numpy?logo=numpy&label=NumPy)](https://pypi.org/project/numpy/)
[![pandas](https://img.shields.io/pypi/v/pandas?logo=pandas&label=pandas)](https://pypi.org/project/pandas/)


## 📚 Table of Contents
- [Pipeline](#pipeline) 
- [Try API](#try-aPI)
- [Demo](#demo)
  - [DemoVideo](#demo-video)
  - [Demo1](#demo1)
- [Setting project locally](#setting-up-project-locally)
  - [Setting up backend locally](#setting-up-backend)



### Pipeline


### Try API

- I have hosted the backend on render **https://baxus-7z5a.onrender.com**
- Test it out using api endpoint 
    - **https://baxus-7z5a.onrender.com/recommend/user/{username}** 
    - **https://baxus-7z5a.onrender.com/recommend/user/{username}?limit=5**
- Username carriebaxus can be tried
    - **https://baxus-7z5a.onrender.com/recommend/user/carriebaxus**

### Demo

#### Demo Video

#### Demo1

On requesting to **https://baxus-7z5a.onrender.com/recommend/user/carriebaxus** I got response as below:

```json
[
  {
    "name": "Jim Beam Black 7 Year",
    "proof": 90,
    "abv": 45,
    "spirit_type": "Bourbon",
    "popularity": 100026,
    "image_url": "https://d1w35me0y6a2bb.cloudfront.net/newproducts/3a40485b-c05d-45ae-bea3-201d0333f373.jpg",
    "avg_msrp": 25,
    "shelf_price": 26.49,
    "ranking": 489,
    "reason": "Similar spirit type: Bourbon | Popular among users"
  },
  {
    "name": "Old Forester Birthday Bourbon 2024",
    "proof": 107,
    "abv": 53.5,
    "spirit_type": "Bourbon",
    "popularity": 100048,
    "image_url": "https://d1w35me0y6a2bb.cloudfront.net/newproducts/48d649f8-c68c-4247-838e-4bbf721b90b8",
    "avg_msrp": 199.99,
    "shelf_price": 1049.5,
    "ranking": 485,
    "reason": "Similar spirit type: Bourbon | Popular among users"
  },
  {
    "name": "Larceny Barrel Proof - Batch B524",
    "proof": 125.4,
    "abv": 62.7,
    "spirit_type": "Bourbon",
    "popularity": 100032,
    "image_url": "https://d1w35me0y6a2bb.cloudfront.net/newproducts/6ebb98ba-6eec-4229-b98b-a70a6b698b7f",
    "avg_msrp": 59.95,
    "shelf_price": 62.46,
    "ranking": 460,
    "reason": "Similar spirit type: Bourbon | Close to your average price ($67.96) | Popular among users | Highly rated"
  }
]
```

### Setting up project locally

#### Setting up backend 

```bash
git clone https://github.com/Davda-James/Agent_BOB
cd Agent_BOB
```
- Installing requirements
```bash 
pip install -r requirements.txt
```
- Start server
```bash
uvicorn agent_bob.app:app --host 127.0.0.1 --port 10000
```

### API Endpoints

- **/** : Just a test api endpoints ensuring server is running

- **/recommend/user/{username}** : Returns the json list containing json ojects of recommended bottles with reason and other attributes.

- **/recommend/user/{username}?limit=5**It also provides query parameter **limit** which is optional.
    - It suggests how many recommendations should be generated.
    - Default value is 3 and max value is 10


