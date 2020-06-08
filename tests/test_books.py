import pytest
from app import create_app, db
from app.models.library import Book, Author


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client  # this is where the testing happens!
    ctx.pop()


@pytest.fixture(scope='module')
def init_database():

    db.create_all()
    test_author = Author(name='Test Author')
    db.session.add(test_author)
    db.session.commit()
    test_book = Book(title='Test book', authors=[1])
    db.session.add(test_book)
    db.session.commit()
    yield db
    db.drop_all()


def test_get_book_by_id(test_client, init_database):
    resp = test_client.get('/books/1')
    assert b'Test book' in resp.data


def test_get_book_by_id_error(test_client, init_database):
    resp = test_client.get('/books/2')
    assert resp.status_code == 404


def test_add_book(test_client, init_database):
    test_data = '{"title": "Test book two", "authors": [1]}'
    resp = test_client.post('/books', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 201


def test_add_book_no_data(test_client, init_database):
    test_data = ''
    resp = test_client.post('/books', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_add_book_not_list(test_client, init_database):
    test_data = '{"title": "Test book two", "authors": 1}'
    resp = test_client.post('/books', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_add_book_assert(test_client, init_database):
    test_data = '{"title": 1, "authors": [1]}'
    resp = test_client.post('/books', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_update_book(test_client, init_database):
    test_data = '{"title": "Test book new"}'
    resp = test_client.put('/books/1', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 200


def test_update_book_no_data(test_client, init_database):
    test_data = ''
    resp = test_client.put('/books/1', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_update_book_no_book(test_client, init_database):
    test_data = '{"title": "Test book new"}'
    resp = test_client.put('/books/6', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 404


def test_update_book_assert(test_client, init_database):
    test_data = '{"title": "Test book new", "authors": 2}'
    resp = test_client.put('/books/1', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_set_book_rating(test_client, init_database):
    test_data = '{"rating": 3}'
    resp = test_client.put('/books/1/rating', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 200


def test_set_book_rating_no_book(test_client, init_database):
    test_data = '{"rating": 3}'
    resp = test_client.put('/books/8/rating', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 404


def test_set_book_rating_no_data(test_client, init_database):
    test_data = ''
    resp = test_client.put('/books/1/rating', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_set_book_rating_error_rating(test_client, init_database):
    test_data = '{"rating": 10}'
    resp = test_client.put('/books/1/rating', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_delete_book(test_client, init_database):
    resp = test_client.delete('/books/1')
    assert resp.status_code == 200


def test_delete_book_wrong(test_client, init_database):
    resp = test_client.delete('/books/7')
    assert resp.status_code == 404
