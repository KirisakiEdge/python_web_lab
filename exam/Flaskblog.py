from datetime import datetime
from flask import Flask
from appInit import db, ma

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    secondname = db.Column(db.String(20), nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    position = db.Column(db.String(60), nullable=False)
    cafedra = db.Column(db.String(60), nullable=False)
    startToWork = db.Column(db.String(60), nullable=False)
    number = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.secondname}', '{self.firstname}')"

class TeacherSchema(ma.Schema):
    class Meta:
        fields = ('id',' secondname','firstname','surname','position', 'cafedra', 'startToWork', 'number')