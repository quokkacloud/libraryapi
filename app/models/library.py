from app import db
from sqlalchemy.orm import validates

DUPLICATE_PARAMETER = '{} with such {} is already in database'
DEFAULT_DICT = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0
}

books_authors = db.Table('books_authors',
                         db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True),
                         db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
                         )


class Author(db.Model):
    """
        Authors model
    """
    __tablename__ = 'authors'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    books = db.relationship("Book", secondary=books_authors, back_populates='authors')

    @property
    def serialized_all(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @property
    def serialized_one(self):
        return {
            'id': self.id,
            'name': self.name,
            'books': [f'{elem.title} - {elem.avg_rating}' for elem in
                      sorted(self.books, key=lambda book: book.avg_rating, reverse=True)[:5]],
        }

    @validates('name')
    def name_validator(self, key, name):
        if not isinstance(name, str):
            raise AssertionError('Wrong format of the field - name')
        if Author.query.filter_by(name=name).first():
            raise AssertionError(DUPLICATE_PARAMETER.format('Author', 'name'))
        return name


class Book(db.Model):
    """
        Books model
    """
    __tablename__ = 'books'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String, nullable=False)
    authors = db.relationship("Author", secondary=books_authors, back_populates='books')
    rating = db.Column(db.PickleType, nullable=False, default=DEFAULT_DICT)
    avg_rating = db.Column(db.Float, nullable=True, default=0.0)

    @property
    def serialized_one(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': [auth.name for auth in self.authors],
            'rating': self.avg_rating
        }

    @property
    def serialized_all(self):
        return {
            'id': self.id,
            'title': self.title,
            # 'authors': [auth.name for auth in self.authors],
            # 'rating': self.get_average_of_ratings(self.rating)
        }

    @property
    def serialized_created(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': [auth.name for auth in self.authors],
            # 'rating': self.get_average_of_ratings(self.rating)
        }

    @validates('title')
    def title_validator(self, key, title):
        if not isinstance(title, str):
            raise AssertionError('Wrong format of the field - title')
        if Book.query.filter_by(title=title).first():
            raise AssertionError(DUPLICATE_PARAMETER.format('Book', 'title'))
        return title

    @validates('authors')
    def authors_validator(self, key, author_id):
        if not isinstance(author_id, int):
            raise AssertionError('Wrong type of the parameter "author"')
        element = Author.query.filter_by(id=author_id).first()
        if not element:
            raise AssertionError(f'There is no author with id {author_id} in database')
        return element







