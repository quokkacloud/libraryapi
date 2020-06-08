from flask_script import Command
from app import db


class InitDatabase(Command):
    """
    Init database command
    """

    def run(self):
        print('Initializing database..')
        db.drop_all()
        db.create_all()
        print('.. Done!')
