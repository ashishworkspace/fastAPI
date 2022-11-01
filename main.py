import random
from typing import Optional
from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel

app = FastAPI()

allPost = []


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    rating: Optional[int]


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    id = random.randrange(0, 1000000)
    postDict = post.dict()
    postDict['id'] = id
    allPost.append(postDict)
    return {
        "msg": "Post created"
    }


@app.get("/posts", status_code=status.HTTP_200_OK)
def getPost():
    return allPost


def returnPostIndexById(id: int) -> int:
    for index, itr in enumerate(allPost):
        if itr["id"] == id:
            return index


@app.get("/posts/latest", status_code=status.HTTP_200_OK)
def getLatestPost():
    if len(allPost) > 0:
        return allPost[len(allPost) - 1]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="POST NOT FOUND")


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def getSinglePost(id: int):
    postIndex = returnPostIndexById(id)
    if postIndex == None:
        raise HTTPException(detail="POST NOT FOUND",
                            status_code=status.HTTP_404_NOT_FOUND)
    return allPost[postIndex]


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteSinglePost(id: int):
    postIndex = returnPostIndexById(id)
    if postIndex == None:
        raise HTTPException(detail="POST NOT FOUND",
                            status_code=status.HTTP_404_NOT_FOUND)
    allPost.pop(postIndex)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def updateSinglePost(id: int, post: Post):
    postIndex = returnPostIndexById(id)
    if postIndex == None:
        raise HTTPException(detail="POST NOT FOUND",
                            status_code=status.HTTP_404_NOT_FOUND)
    postDict = post.dict()
    postDict['id'] = id
    allPost[postIndex] = postDict
    return {
        "msg": "update successfully"
    }
