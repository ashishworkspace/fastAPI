from ast import While
import random
from typing import Optional
from database import SessionLocal
from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session 

app = FastAPI()

allPost = []

while True:
    try:
        conn = psycopg2.connect(database='postgres', user='postgres',
                                password='password', host='sql-postgres', cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Database connected successfully.")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error", error)
        time.sleep(2)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/sqlalchemy")
def sqlAlchemy(db: Session = Depends(get_db)):
    return {
        "database": "connected",
        "status": "OK"
    }

class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    rating: Optional[int]


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    cur.execute("""INSERT INTO media (title, content) VALUES (%s, %s)""",
                (post.title, post.content))
    conn.commit()
    return {
        "msg": "Post created"
    }


@app.get("/posts", status_code=status.HTTP_200_OK)
def getPost():
    cur.execute("SELECT * FROM media")
    posts = cur.fetchall()
    return posts


def returnPostIndexById(id: int) -> int:
    for index, itr in enumerate(allPost):
        if itr["id"] == id:
            return index


@app.get("/posts/latest", status_code=status.HTTP_200_OK)
def getLatestPost():
    cur.execute("SELECT COUNT(*) FROM media")
    count = cur.fetchall()
    if count[0]['count'] > 0:
        cur.execute(" SELECT * FROM media ORDER BY id DESC LIMIT 1")
        record = cur.fetchall()
        return record
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="POST NOT FOUND")


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def getSinglePost(id: str):
    cur.execute("""SELECT * FROM media WHERE id = %s""", (str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(detail="POST NOT FOUND",
                            status_code=status.HTTP_404_NOT_FOUND)
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteSinglePost(id: int):
    cur.execute("DELETE FROM media WHERE id = %s RETURNING *", str(id))
    post = cur.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(detail="POST NOT FOUND",
                            status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def updateSinglePost(id: int, post: Post):
    cur.execute("UPDATE media SET title = %s , content = %s WHERE id = %s RETURNING *",
                (post.title, post.content, str(id)))
    post = cur.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(detail="POST NOT FOUND",
                            status_code=status.HTTP_404_NOT_FOUND)
    return {
        "msg": "update successfully"
    }
