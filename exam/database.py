from flask_script import Manager, prompt_bool, Command
from appInit import db

manager = Manager(usage = "Perform databse operations")

@manager.command
def drop():
	db.drop_all()

@manager.command
def createdb():
	db.create_all()

@manager.command
def recreate():
	dropdb()
	createdb()

@manager.command
def initData():
	print("iniitialization completed")


