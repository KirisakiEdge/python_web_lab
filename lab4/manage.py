from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager 
from flask_script import Command, prompt_bool

from appInit import app, db

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from database import manager as databaseManager
manager.add_command("database", databaseManager)

if __name__ == '__main__':
	manager.run()