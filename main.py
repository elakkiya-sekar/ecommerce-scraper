import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app=FastAPI()

app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_methods=["*"],
     allow_headers=["*"],
)

def get_db_connection():
    connection=sqlite3.connect("books_database.db")
    connection.row_factory=sqlite3.Row
    return connection


@app.get("/")
def read_root():
    return FileResponse("index.html")


@app.get("/books")
def get_books(title: str = None, rating: str=None, max_price: float=None):
    query="SELECT id, title, price, rating FROM book_database WHERE 1=1"
    param=[]
    if rating:
        query+=" AND rating=?"
        param.append(rating)
    if max_price:
         query+=" AND price <=?"
         param.append(max_price)
    if title:
        query+=" AND title LIKE ?"
        param.append(f"{title.strip()}%")
   
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute(query, param)
           
    rows=cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
