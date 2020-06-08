#!/usr/bin/env python
from flask_migrate import MigrateCommand
from flask_script import Manager
from app import create_app
from app.commands import InitDatabase

# Setup Flask-Script with command line commands
manager = Manager(create_app)
manager.add_command('db', MigrateCommand)
manager.add_command('init_db', InitDatabase)


if __name__ == "__main__":
    """
        Run application
    """
    manager.run()
