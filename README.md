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
- (Try API)[Try API]
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


