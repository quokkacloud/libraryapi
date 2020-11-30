# LIBRARY
## Code characteristics

    Works on Python 3.7

## Setting up a development environment

    # Install required Python packages 
    pip install -r requirements-test.txt
    pip install -r requirements-dev.txt
    
## Unit tests

    # To run unit test 
    pytest /tests/*

## Initializing the Database

    # Create DB tables and populate the tables
    python manage.py db upgrade

## Running the app

    # Start the Flask development web server
    python manage.py runserver
    
## Create authors and books 
    sh curls_commands_for_db.sh

# TESTING

    # You need `curl` to test API
    apt-get install curl
    
## Authors

    # Show all authors or with parameters page and per_page for pagination
    curl -X GET http://localhost:5000/authors
    curl -X GET http://localhost:5000/authors?page=<page number>&per_page=<fields per page>
    
    # Show one author and top 5 of his books
    curl -X GET http://localhost:5000/authors/<id>
    
    # Create new author
    curl -d '{"name": "New Author"}' -i -H "Content-Type: application/json" -X POST http://localhost:5000/authors

    # Update author
    curl -d '{"name": "Update Author"}' -i -H "Content-Type: application/json" -X PUT http://localhost:5000/authors/<id>

    # Delete author
    curl -X DELETE http://localhost:5000/authors/<id>

## Books

    # Show all books or with parameters page and per_page for pagination
    curl -X GET http://localhost:5000/books
    curl -X GET http://localhost:5000/books?page=<page number>&per_page=<fields per page>
    
    # Show one book with it's avg rating
    curl -X GET http://localhost:5000/books/<id>
    
    # Create new book
    curl -d '{"title": "New Book", "authors": [<authors_id>]}' -i -H "Content-Type: application/json" -X POST http://localhost:5000/books

    # Update book
    curl -d '{"title": "Update Book", "authors": [<authors_id>]}' -i -H "Content-Type: application/json" -X PUT http://localhost:5000/books/<id>

    # Delete book
    curl -X DELETE http://localhost:5000/books/<id>
    
    # Set rating to the book
    curl -d '{"rating": <ingerer from 1 to 5>}' -i -H "Content-Type: application/json" -X PUT http://localhost:5000/books/<id>/rating
    
