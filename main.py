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
def get_all_books():
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM book_database")
        rows=cursor.fetchall()
        conn.close()
        books = []
        for row in rows:
            books.append({
            "id": row[0],
            "title": row[1],
            "price": row[2],
            "rating": row[3]
        })
        return books