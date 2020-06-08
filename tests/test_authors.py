import pytest
from app import create_app, db
from flask import jsonify
from app.models.library import Author


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
    yield db
    db.drop_all()


def test_get_author_by_id(test_client, init_database):
    resp = test_client.get('/authors/1')
    assert b'Test Author' in resp.data


def test_get_author_by_id_error(test_client, init_database):
    resp = test_client.get('/authors/2')
    assert resp.status_code == 404


def test_add_author(test_client, init_database):
    test_data = '{"name": "Test Author Two"}'
    resp = test_client.post('/authors', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 201


def test_add_author_no_data(test_client, init_database):
    test_data = ''
    resp = test_client.post('/authors', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_add_author_dup(test_client, init_database):
    test_data = '{"name": "Test Author"}'
    resp = test_client.post('/authors', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_update_author(test_client, init_database):
    test_data = '{"name": "Test Author New"}'
    resp = test_client.put('/authors/1', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 200


def test_update_author_no_data(test_client, init_database):
    test_data = ''
    resp = test_client.put('/authors/1', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_update_author_no_author(test_client, init_database):
    test_data = '{"name": "Test Author New"}'
    resp = test_client.put('/authors/6', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 404


def test_update_author_assert(test_client, init_database):
    test_data = '{"name": 1}'
    resp = test_client.put('/authors/1', data=test_data, headers={'Content-Type': 'application/json'})
    assert resp.status_code == 400


def test_delete_author(test_client, init_database):
    resp = test_client.delete('/authors/1')
    assert resp.status_code == 200


def test_delete_author_error(test_client, init_database):
    resp = test_client.delete('/authors/7')
    assert resp.status_code == 404
