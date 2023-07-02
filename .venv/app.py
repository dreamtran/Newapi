from flask import Flask 
from flask import request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(1000))
    author = db.Column(db.String(200))
    publisher = db.Column(db.String(200))

    def __repr__(self):
        return f"{self.book_name} - {self.author}"


@app.route('/')
def index():
    return "Hello!"

@app.route('/books')
def get_books():
    
    all_books = Book.query.all()
    output = []
    for book in all_books:
        # Process the data and return a response
        book_data = [{"book_name": book.book_name, "author": book.author, "publisher": book.publisher} for book in all_books]
        output.append(book_data)
    return {"books": output}


@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"book_name": book.book_name, "author": book.author}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['book_name'], author=request.json['author'])
    db.session.add(book)
    db.session.commit()
    return "Added"

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return "404"
    db.session.delete(book)
    db.session.commit()
    return "Done"

