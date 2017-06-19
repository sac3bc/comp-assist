from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)

## SQLAlchemy Models will live here... So replace the below User model with the
## example if you wish to play with it.
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    articles = db.relationship('Book', backref='author')

    def __repr__(self):
        return '<Author:{}>'.format(self.name)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __repr__(self):
        return '<Book:{}>'.format(self.title)

## Then we'll run in an app context to work with the ORM:
if __name__ == '__main__':
   db.create_all()
   # app.run(debug = True)
   app.run()