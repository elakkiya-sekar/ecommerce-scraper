import sqlite3
from fastapi import FastAPI

app=FastAPI()

def get_db_connection():
    connection=sqlite3.connect("books_database.db")
    connection.row_factory=sqlite3.Row
    return connection


@app.get("/")
def read_root():
    return {"message":"API is live"}


@app.get("/books")
def get_all_books():
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM book_database")
        rows=cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]