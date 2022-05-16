

class HiredEmployeeRepository():
    def __init__(self, session):
        self.session = session

    def create(self, hired_employee):
        self.session.add(hired_employee)

class DepartmentRepository():
    def __init__(self, session):
        self.session = session

    def create(self, department):
        self.session.add(department)

class JobRepository():
    def __init__(self, session):
        self.session = session

    def create(self, job):
        self.session.add(job)
