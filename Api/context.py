from .repositories import HiredEmployeeRepository, DepartmentRepository, JobRepository


class Context():

    def __init__(self, session):
        self.session = session
        self.hiredEmployeeRepository = HiredEmployeeRepository(self.session)
        self.departmentRepository = DepartmentRepository(self.session)
        self.jobRepository = JobRepository(self.session)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()