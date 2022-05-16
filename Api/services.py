from csv import reader
from .models import HiredEmployees, Departments, Jobs
from .context import Context
from .logger import logger


class HiredEmployeeService():

    def __init__(self, context: Context):
        self.context = context

    def validateHiredEmployee(self, hiredEmployee, index):
        error_messages = [f"Record index: {index}"]
        if 'id' not in hiredEmployee or hiredEmployee['id']=='':
            error_messages.append(f"The field ID is required.")
        if 'name' not in hiredEmployee or hiredEmployee['name']=='':
            error_messages.append(f"The field NAME is required.")
        if 'datetime' not in hiredEmployee or hiredEmployee['datetime']=='':
            error_messages.append(f"The field DATETIME is required.")
        if 'department_id' not in hiredEmployee or hiredEmployee['department_id']=='':
            error_messages.append(f"The field DEPARMENT_ID is required.")
        if 'job_id' not in hiredEmployee or hiredEmployee['job_id']=='':
            error_messages.append(f"The field JOB_ID is required.")

        if len(error_messages) > 1:
            logger.info('\n'.join(error_messages))
            return False
        return True

    def createHiredEmployeesBash(self, hiredEmployees):
        index = 0
        for hiredEmployee in hiredEmployees:
            if self.validateHiredEmployee(hiredEmployee, index):
                newHiredEmployee = HiredEmployees(hiredEmployee['id'], hiredEmployee['name'], hiredEmployee['datetime'], hiredEmployee['department_id'], hiredEmployee['job_id'])
                self.context.hiredEmployeeRepository.create(newHiredEmployee)
            index += 1
        self.context.commit()

    def createHiredEmployeesFromCSV(self, path):
        index = 0
        with open(path, 'r') as file:
            hiredEmployees = reader(file)
            for hiredEmployee in hiredEmployees:
                if self.validateHiredEmployee({'id':int(hiredEmployee[0]), 'name':hiredEmployee[1], 'datetime':hiredEmployee[2], 'department_id':hiredEmployee[3], 'job_id':hiredEmployee[4]}, index):
                    newHiredEmployee = HiredEmployees(hiredEmployee[0], hiredEmployee[1], hiredEmployee[2], hiredEmployee[3], hiredEmployee[4])
                    self.context.hiredEmployeeRepository.create(newHiredEmployee)
                index += 1
        self.context.commit()

class DepartmentService():

    def __init__(self, context):
        self.context = context

    def validateDepartment(self, department, index):
        error_messages = [f"Record index: {index}"]
        if 'id' not in department:
            error_messages.append(f"The field ID is required.")
        if 'department' not in department:
            error_messages.append(f"The field DEPARMENT is required.")

        if len(error_messages) > 1:
            logger.info('\n'.join(error_messages))
            return False
        return True

    def createDepartmentsBash(self, departments):
        index = 0
        for department in departments:
            if self.validateDepartment(department, index):
                newDepartment = Departments(department['id'], department['department'])
                self.context.departmentRepository.create(newDepartment)
            index += 1
        self.context.commit()

    def createDepartmentsFromCSV(self, path):
        index = 0
        with open(path, 'r') as file:
            departments = reader(file)
            for department in departments:
                if self.validateDepartment({'id':int(department[0]), 'department':department[1]}, index):
                    newDepartment = Departments(int(department[0]), department[1])
                    self.context.departmentRepository.create(newDepartment)
                index += 1
        self.context.commit()

class JobService():

    def __init__(self, context):
        self.context = context

    def validateJob(self, job, index):
        error_messages = [f"Record index: {index}"]
        if 'id' not in job:
            error_messages.append(f"The field ID is required.")
        if 'job' not in job:
            error_messages.append(f"The field JOB is required.")

        if len(error_messages) > 1:
            logger.info('\n'.join(error_messages))
            return False
        return True

    def createJobsBash(self, jobs):
        index = 0
        for job in jobs:
            if self.validateJob(job, index):
                newJob = Jobs(job['id'], job['job'])
                self.context.jobRepository.create(newJob)
            index += 1
        self.context.commit()

    def createJobsFromCSV(self, path):
        index = 0
        with open(path, 'r') as file:
            jobs = reader(file)
            for job in jobs:
                if self.validateJob({'id':int(job[0]), 'job':job[1]}, index):
                    newJob = Jobs(int(job[0]), job[1])
                    self.context.jobRepository.create(newJob)
                index += 1
        self.context.commit()

class ReportService():

    def __init__(self, context):
        self.context = context

    def hired_employees_by_job_department_quarter(self):
        query = '''
            select department, job,
            sum(Q1) as Q1,
            sum(Q2) as Q2,
            sum(Q3) as Q3,
            sum(Q4) as Q4
            from (
                select a.department, c.job,
                case when extract(quarter from to_date(b.datetime, 'YYYY-MM-DD')) = 1 then 1 else 0 end as Q1,
                case when extract(quarter from to_date(b.datetime, 'YYYY-MM-DD')) = 2 then 1 else 0 end as Q2,
                case when extract(quarter from to_date(b.datetime, 'YYYY-MM-DD')) = 3 then 1 else 0 end as Q3,
                case when extract(quarter from to_date(b.datetime, 'YYYY-MM-DD')) = 4 then 1 else 0 end as Q4
                from departments a
                inner join hired_employees b on a.id = b.department_id
                inner join jobs c on b.job_id = c.id
                where to_char(to_date(b.datetime, 'YYYY-MM-DD'), 'YYYY') = '2021'
            ) a
            group by department, job
            order by department, job;
        '''

        result_list = []
        for result in self.context.session.execute(query):
            result_list.append({'department':result[0], 'job':result[1], 'Q1':result[2], 'Q2':result[3], 'Q3':result[4], 'Q4':result[5] })
        return result_list

    def hired_employees_by_department_over_median(self):
        query_median = '''
            select avg(hired) as median_hired
            from (
                select a.department, count(*) as hired
                from departments a
                inner join hired_employees b on a.id = b.department_id
                where to_char(to_date(b.datetime, 'YYYY-MM-DD'), 'YYYY') = '2021'
                group by a.department
            ) a;
        '''

        median = self.context.session.execute(query_median).fetchone()

        query = '''
            select a.department, count(*) as hired
            from departments a
            inner join hired_employees b on a.id = b.department_id
            group by a.department
            having count(*) > {MEDIAN}
            order by 2 desc;
        '''.format(MEDIAN=int(median['median_hired']))

        result_list = []
        for result in self.context.session.execute(query):
            result_list.append({'department':result[0], 'hired':result[1]})
        return result_list
