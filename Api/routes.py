from flask import Blueprint, request, jsonify
from .services import HiredEmployeeService, DepartmentService, JobService, ReportService
from . import get_context


bp = Blueprint('api', __name__)

@bp.route('/hired-employees/bash-loading', methods=['POST'])
def hired_employee_bash_loading():
   data_request = request.get_json()
   context = get_context()
   hiredEmployeeService = HiredEmployeeService(context)
   hiredEmployeeService.createHiredEmployeesBash(data_request)
   return jsonify({"msg": "Hired Employees created"})

@bp.route('/hired-employees/csv-loading', methods=['POST'])
def hired_employee_csv_loading():
   data_request = request.get_json()
   context = get_context()
   hiredEmployeeService = HiredEmployeeService(context)
   hiredEmployeeService.createHiredEmployeesFromCSV(data_request['path_data'])
   return jsonify({"msg": "Hired Employees created"})

@bp.route('/departments/bash-loading', methods=['POST'])
def department_bash_loading():
   data_request = request.get_json()
   context = get_context()
   departmentService = DepartmentService(context)
   departmentService.createDepartmentsBash(data_request)
   return jsonify({"msg": "Departments created"})

@bp.route('/departments/csv-loading', methods=['POST'])
def department_csv_loading():
   data_request = request.get_json()
   context = get_context()
   departmentService = DepartmentService(context)
   departmentService.createDepartmentsFromCSV(data_request['path_data'])
   return jsonify({"msg": "Departments created"})

@bp.route('/jobs/bash-loading', methods=['POST'])
def jobs_bash_loading():
   data_request = request.get_json()
   context = get_context()
   jobService = JobService(context)
   jobService.createJobsBash(data_request)
   return jsonify({"msg": "Jobs created"})

@bp.route('/jobs/csv-loading', methods=['POST'])
def jobs_csv_loading():
   data_request = request.get_json()
   context = get_context()
   jobService = JobService(context)
   jobService.createJobsFromCSV(data_request['path_data'])
   return jsonify({"msg": "Jobs created"})

@bp.route('/reports/hired-employees-by-job-department-quarter', methods=['GET'])
def get_hired_employees_by_job_department_quarter():
   context = get_context()
   reportService = ReportService(context)
   return jsonify(reportService.hired_employees_by_job_department_quarter())

@bp.route('/reports/hired-employees-by-department-over-median', methods=['GET'])
def get_hired_employees_by_department_over_median():
   context = get_context()
   reportService = ReportService(context)
   return jsonify(reportService.hired_employees_by_department_over_median())
