import sqlite3
from  bs4 import BeautifulSoup
import requests

url="http://books.toscrape.com/catalogue/page-1.html"
response=requests.get(url)
response.encoding = "utf-8"

connection=sqlite3.connect("books_database.db")
cursor=connection.cursor()

cursor.execute(" CREATE TABLE IF NOT EXISTS book_database(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT,price REAL,rating TEXT,date_scraped TIMESTAMP  DEFAULT CURRENT_TIMESTAMP)")


content=BeautifulSoup(response.text, "html.parser")

book= content.find_all('article', class_='product_pod')

for books in book:
    link=books.find("h3").find("a")
    link=link["title"]
    

    prices=books.find('p',class_='price_color').text.strip()
    price_text=prices.replace("£", "")
    price=float(price_text)

    rating=books.find('p',class_='star-rating')["class"][1]

    cursor.execute("INSERT INTO book_database (title, price, rating) VALUES(?,?,?)",(link,price,rating,))

connection.commit()

cursor.execute("SELECT * FROM book_database")
print(cursor.fetchall())

connection.close()