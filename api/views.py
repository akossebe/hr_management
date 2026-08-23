from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from employees.models import Employee, Department, Position
from leaves.models import LeaveRequest, LeaveType
from payroll.models import Payslip
from attendance.models import Attendance
from .serializers import (
    EmployeeSerializer, DepartmentSerializer, PositionSerializer,
    LeaveRequestSerializer, LeaveTypeSerializer, PayslipSerializer, AttendanceSerializer
)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department', 'position').all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'registration_number', 'email']


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.select_related('employee', 'leave_type').all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PayslipViewSet(viewsets.ModelViewSet):
    queryset = Payslip.objects.select_related('employee').all()
    serializer_class = PayslipSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('employee').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
