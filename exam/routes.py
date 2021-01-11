from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SelectField, TextField
from wtforms.validators import InputRequired, Length, AnyOf
from Flaskblog import Teacher, TeacherSchema
from appInit import app, db 
import database
from sqlalchemy import desc, asc
from flask_restful import Api
from flask import jsonify, request
from flask_restful import Resource
import json 

#database.drop()
database.createdb()

class teacherForm(FlaskForm):
    secondname = StringField('Secondname', validators=[InputRequired('A name is REQUIRED!'),
                                               Length(min=3, max=20, message='Must be filled')])

    firstname = StringField('Firstname', validators=[InputRequired('A name is REQUIRED!'),
                                               Length(min=3, max=20, message='Must be filled')])

    surname = StringField('Surname', validators=[InputRequired('A name is REQUIRED!'),
                                               Length(min=5, max=20, message='Must be filled')])

    position = SelectField('Posotion', choices=[("Асистент", "Асистент"), 
      ("Викладач", "Викладач"), 
      ("Доцент", "Доцент"), 
      ("Професор", "Професор")])

    cafedra = StringField('Cafedra', validators=[InputRequired('A name is REQUIRED!'),
                                               Length(min=5, max=20, message='Must be filled')])

    startToWork = StringField('Start to work', validators=[InputRequired('A name is REQUIRED!'),
                                               Length(min=3, max=20, message='Must be filled')])

    number = StringField('Number', validators=[InputRequired('A name is REQUIRED!'),
                                               Length(min=10, max=15, message='Must be filled')])


@app.route('/')
def base():
  return render_template('base.html')

@app.route('/teacherList', methods=['GET', 'POST']) 
def teacherList():
  query = Teacher.query.order_by(asc(Teacher.firstname))
  return render_template('teacherList.html', title = 'All Teacher', query = query)


@app.route('/addTeacher', methods=['GET', 'POST']) 
def addTeacher():
  addTeacher = teacherForm()
  if addTeacher.validate_on_submit():
    teacher = Teacher()
    if Teacher.query.filter_by(number = format(addTeacher.number.data)).first() == None:
      teacher.secondname = format(addTeacher.secondname.data)
      teacher.firstname = format(addTeacher.firstname.data)
      teacher.surname = format(addTeacher.surname.data)
      teacher.position = format(addTeacher.position.data)
      teacher.cafedra = format(addTeacher.cafedra.data)
      teacher.startToWork = format(addTeacher.startToWork.data)
      teacher.number = format(addTeacher.number.data)
      db.session.add(teacher)
      db.session.commit()
      flash(f'Teacher add for {addTeacher.firstname.data}!', category = 'success')
      return redirect(url_for('teacherList'))
    else:
      flash(f'This teacher already exist', category = 'success')
  return render_template('addTeacher.html', addTeacher=addTeacher)



class GetTeachers(Resource):
  def get(self):
    teacher = db.session.query(Teacher).all()
    result = TeacherSchema(many=True).dump(teacher)
    return jsonify(result)



class GetTeacher(Resource):
  def post(self, id):
    teacher = Teacher(id =id,secondname='aaa',firstname='fff',surname='sss',
      position='fff',cafedra='ggg',startToWork='ggg',number='xxx')
    db.session.add(teacher)
    db.session.commit()
    result = TeacherSchema().dump(teacher)
    return jsonify(result)

  def get(self, id):
    teacher = Teacher.query.filter_by(id=id).first()
    result = TeacherSchema().dump(teacher)
    return jsonify(result)

  def put(self, id):
    teacher = Teacher.query.filter_by(id=id).first()
    teacher.surname = 'ooooooo'
    db.session.commit()
    result = TeacherSchema().dump(teacher)
    return jsonify(result)

  def delete(self, id):
    teacher = Teacher.query.filter_by(id=id).first()
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({'message': 'The user has been deleted!'})


api = Api(app)
api.add_resource(GetTeacher, '/api/teacher/<string:id>')
api.add_resource(GetTeachers, '/api/teachers')

if __name__ == '__main__':
  app.run(debug=True)