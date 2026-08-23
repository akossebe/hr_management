from rest_framework import serializers
from employees.models import Employee, Department, Position
from leaves.models import LeaveRequest, LeaveType
from payroll.models import Payslip
from attendance.models import Attendance

class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(source='employees.count', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'manager', 'employee_count']


class PositionSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Position
        fields = ['id', 'title', 'department', 'department_name', 'base_salary_min', 'base_salary_max']


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')
    position_title = serializers.ReadOnlyField(source='position.title')
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            'id', 'registration_number', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'gender', 'marital_status', 'address',
            'department', 'department_name', 'position', 'position_title',
            'contract_type', 'status', 'hire_date', 'base_salary'
        ]


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.full_name')
    leave_type_name = serializers.ReadOnlyField(source='leave_type.name')
    duration_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name', 'leave_type', 'leave_type_name',
            'start_date', 'end_date', 'duration_days', 'reason', 'status', 'hr_comment'
        ]


class PayslipSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.full_name')
    month_name = serializers.CharField(source='get_month_display', read_only=True)

    class Meta:
        model = Payslip
        fields = [
            'id', 'employee', 'employee_name', 'month', 'month_name', 'year',
            'basic_salary', 'transport_allowance', 'housing_allowance', 'performance_bonus',
            'gross_salary', 'tax_deduction', 'social_security_deduction', 'net_salary',
            'payment_date', 'payment_method', 'status'
        ]


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.full_name')

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'date', 'time_in', 'time_out', 'status', 'notes'
        ]
