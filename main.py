from fastapi import FastAPI
from models1.book import Book

app=FastAPI()

@app.get('/book')
def index(availabel:bool='True'):
    if availabel:
        return {'data':'availabel books'}
    return {'data':'All books'}


@app.get('/book/{id}')
def index(id):
    return {'data':id}


@app.post('/book')
def add_book(request: Book):
    return {'data':f"{request.title} Book is added"}






