import random
from typing import Optional
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

allPost = []

class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    rating: Optional[int]

# POST 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    id = random.randrange(0, 1000000)
    postDict = post.dict()
    postDict['id'] = id
    allPost.append(post)
    return {
        "msg": "Post created"
    }


# GET
@app.get("/posts", status_code=status.HTTP_200_OK)
def getPost():
    return allPost
