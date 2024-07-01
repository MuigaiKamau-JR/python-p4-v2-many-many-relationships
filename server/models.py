# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Define the association table for employee_meetings
employee_meetings = Table('employee_meetings', db.Model.metadata,
    db.Column('employee_id', db.Integer, db.ForeignKey('employees.id')),
    db.Column('meeting_id', db.Integer, db.ForeignKey('meetings.id'))
)

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hire_date = db.Column(db.Date)

    meetings = db.relationship(
        'Meeting', secondary=employee_meetings, back_populates='employees')

    assignments = db.relationship(
        'Assignment', back_populates='employee', cascade='all, delete-orphan')

    projects = relationship(
        'Project', secondary='assignments', back_populates='employees')

    def __repr__(self):
        return f'<Employee {self.id}, {self.name}, {self.hire_date}>'


class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    scheduled_time = db.Column(db.DateTime)
    location = db.Column(db.String)

    employees = db.relationship(
        'Employee', secondary=employee_meetings, back_populates='meetings')

    def __repr__(self):
        return f'<Meeting {self.id}, {self.topic}, {self.scheduled_time}, {self.location}>'


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    budget = db.Column(db.Integer)

    assignments = db.relationship(
        'Assignment', back_populates='project', cascade='all, delete-orphan')

    employees = relationship(
        'Employee', secondary='assignments', back_populates='projects')

    def __repr__(self):
        return f'<Project {self.id}, {self.title}, {self.budget}>'


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    employee = db.relationship('Employee', back_populates='assignments')
    project = db.relationship('Project', back_populates='assignments')

    def __repr__(self):
        return f'<Assignment {self.id}, {self.role}, {self.start_date}, {self.end_date}, Employee ID: {self.employee_id}, Project ID: {self.project_id}>'
