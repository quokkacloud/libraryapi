import json
from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.library import Book
from app.utils import get_average_of_ratings

RATING_LIST = [1, 2, 3, 4, 5]
NO_BOOK_FOUND = 'There is no book with id {} in database'
BOOKS_PER_PAGE = 10

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/books', methods=['GET'])
def get_all_books():
    """
        Get all books from database

        :return:
            Response in Json format
    """
    page = request.args.get('page')
    per_page = request.args.get('per_page')
    if page and per_page:
        result = Book.query.paginate(int(page), per_page=int(per_page))
        return make_response(jsonify({"result": [author.serialized_all for author in result.items]}), 200)
    else:
        return make_response(jsonify({"result": [author.serialized_all for author in Book.query.all()]}), 200)


@books_blueprint.route('/books/<int:idx>', methods=['GET'])
def get_book_by_id(idx):
    """
        Get all book from database

        :param idx: book's id

        :return:
            Response in Json format
    """

    result = Book.query.filter_by(id=idx).first()
    if not result:
        return make_response(jsonify({"error": NO_BOOK_FOUND.format(idx)}), 404)
    return make_response(jsonify({"result": result.serialized_one}), 200)


@books_blueprint.route('/books', methods=['POST'])
def add_book():
    """
        Add new book

        :return:
            Response in Json format
    """
    if not request.data:
        return make_response(jsonify({"error": 'Bad request'}), 400)
    data = json.loads(request.data)
    authors = data.get('authors')
    if not isinstance(authors, list):
        return make_response(jsonify({"error": 'Parameter "authors" must be list of int'}), 400)
    try:
        element = Book(title=data.get('title'), authors=authors)
        db.session.add(element)
        db.session.commit()
        return make_response(jsonify({"result": element.serialized_one}), 201)
    except AssertionError as err:
        return make_response(jsonify({"error": str(err)}), 400)


@books_blueprint.route('/books/<int:idx>', methods=['PUT'])
def update_book(idx):
    """
        Update book

        :param idx: book's id

        :return:
            Response in Json format
    """
    if not request.data:
        return make_response(jsonify({"error": 'Bad request'}), 400)
    element = Book.query.filter_by(id=idx).first()
    if not element:
        return make_response(jsonify({"error": NO_BOOK_FOUND.format(idx)}), 404)
    data = json.loads(request.data)
    authors = data.get('authors')
    title = data.get('title')
    try:
        if authors:
            if not isinstance(authors, list):
                return make_response(jsonify({"error": 'Parameter "authors" must be list of int'}), 400)
            element.authors = authors
        if title:
            element.title = title
        db.session.commit()
        return make_response(jsonify({"result": 'Updated'}), 200)
    except AssertionError as err:
        return make_response(jsonify({"error": str(err)}), 400)


@books_blueprint.route('/books/<int:idx>', methods=['DELETE'])
def delete_book(idx):
    """
        Delete book

        :param idx: book's id

        :return:
            Response in Json format
    """
    element = Book.query.filter_by(id=idx).first()
    if not element:
        return make_response(jsonify({"error": NO_BOOK_FOUND.format(idx)}), 404)
    db.session.delete(element)
    db.session.commit()
    return make_response(jsonify({"result": 'Book deleted'}), 200)


@books_blueprint.route('/books/<int:idx>/rating', methods=['PUT'])
def set_book_rating(idx):
    """
        Set book rating

        :param idx: book's id

        :return:
            Response in Json format
    """

    element = Book.query.filter_by(id=idx).first()
    if not element:
        return make_response(jsonify({"error": NO_BOOK_FOUND.format(idx)}), 404)
    if not request.data:
        return make_response(jsonify({"error": 'Bad request'}), 400)
    rating = json.loads(request.data).get('rating')
    if rating not in RATING_LIST:
        return make_response(jsonify({"error": 'Rating must be integer from 1 to 5'}), 400)
    new_rating = dict(element.rating)
    new_rating[rating] += 1
    element.rating = dict(new_rating)
    element.avg_rating = get_average_of_ratings(element.rating)
    db.session.commit()
    return make_response(jsonify({"result": 'Rate is set'}), 200)
