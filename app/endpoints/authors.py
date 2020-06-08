import json
from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.library import Author

NO_AUTH_FOUND = 'There is no author with id {} in database'
AUTHORS_PER_PAGE = 10

authors_blueprint = Blueprint('authors', __name__)


@authors_blueprint.route('/authors', methods=['GET'])
def get_all_authors():
    """
        Get all authors from database

        :return:
            Response in Json format
    """
    page = request.args.get('page')
    per_page = request.args.get('per_page')
    if page and per_page:
        result = Author.query.paginate(int(page), per_page=int(per_page))
        return make_response(jsonify({"result": [author.serialized_all for author in result.items]}), 200)
    else:
        return make_response(jsonify({"result": [author.serialized_all for author in Author.query.all()]}), 200)


@authors_blueprint.route('/authors/<int:idx>', methods=['GET'])
def get_author_by_id(idx):
    """
        Get author by id from database

        :param idx: author id

        :return:
            Response in Json format
    """

    result = Author.query.filter_by(id=idx).first()
    if not result:
        return make_response(jsonify({"error": NO_AUTH_FOUND.format(idx)}), 404)
    return make_response(jsonify({"result": result.serialized_one}), 200)


@authors_blueprint.route('/authors', methods=['POST'])
def add_author():
    """
        Add new author to database

        :return:
            Response in Json format

    """
    if not request.data:
        return make_response(jsonify({"error": 'Bad request'}), 400)
    data = json.loads(request.data)
    try:
        element = Author(name=data.get('name'))
        db.session.add(element)
        db.session.commit()
        # element.id
        return make_response(jsonify({"result": element.serialized_all}), 201)
    except AssertionError as err:
        return make_response(jsonify({"error": str(err)}), 400)


@authors_blueprint.route('/authors/<int:idx>', methods=['PUT'])
def update_author(idx):
    """
        Update author in database

        :param idx: author id

        :return:
            Response in Json format

    """
    if not request.data:
        return make_response(jsonify({"error": 'Bad request'}), 400)
    data = json.loads(request.data)
    element = Author.query.filter_by(id=idx).first()
    if not element:
        return make_response(jsonify({"error": NO_AUTH_FOUND.format(idx)}), 404)
    try:
        element.name = data.get("name")
        db.session.commit()
        return make_response(jsonify({"result": 'Updated'}), 200)
    except AssertionError as err:
        return make_response(jsonify({"error": str(err)}), 400)


@authors_blueprint.route('/authors/<int:idx>', methods=['DELETE'])
def delete_author(idx):
    """
        Delete author from database

        :param idx: author id

        :return:
            Response in Json format

    """

    element = Author.query.filter_by(id=idx).first()
    if not element:
        return make_response(jsonify({"error": NO_AUTH_FOUND.format(idx)}), 404)
    db.session.delete(element)
    db.session.commit()
    return make_response(jsonify({"result": 'Author deleted'}), 200)



