from sqlalchemy import ForeignKey
from . import db
from sqlalchemy.orm import relationship


class HiredEmployees(db.Model):
    __tablename__ = 'hired_employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    datetime = db.Column(db.String, nullable=False)
    department_id = db.Column(db.Integer, ForeignKey('departments.id'), nullable=False)
    department = relationship("Departments", back_populates="hired_employees")
    job_id = db.Column(db.Integer, ForeignKey('jobs.id'), nullable=False)
    job = relationship("Jobs", back_populates="hired_employees")


    def __init__(self, id, name, datetime, department_id, job_id):
        self.id = id
        self.name = name
        self.datetime = datetime
        self.department_id = department_id
        self.job_id = job_id

class Departments(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String, nullable=False)
    hired_employees = relationship("HiredEmployees")

    def __init__(self, id, department):
        self.id = id
        self.department = department

class Jobs(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String, nullable=False)
    hired_employees = relationship("HiredEmployees")

    def __init__(self, id, job):
        self.id = id
        self.job = job
