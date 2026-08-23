from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.utils import timezone
from employees.models import Employee, Department
from leaves.models import LeaveRequest
from payroll.models import Payslip

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(status='ACTIF').count()
    on_leave_employees = Employee.objects.filter(status='EN_CONGE').count()
    departments_count = Department.objects.count()
    
    # Monthly Payroll total
    current_year = timezone.now().year
    current_month = timezone.now().month
    total_payroll_net = Payslip.objects.filter(year=current_year, month=current_month).aggregate(Sum('net_salary'))['net_salary__sum'] or 0

    # Department breakdown for charts
    dept_stats = Department.objects.annotate(emp_count=Count('employees')).values('name', 'emp_count')
    dept_labels = [d['name'] for d in dept_stats]
    dept_data = [d['emp_count'] for d in dept_stats]

    # Leave requests breakdown
    pending_leaves = LeaveRequest.objects.filter(status='EN_ATTENTE').count()
    approved_leaves = LeaveRequest.objects.filter(status='APPROUVE').count()
    rejected_leaves = LeaveRequest.objects.filter(status='REFUSE').count()

    # Recent lists
    recent_employees = Employee.objects.select_related('department', 'position').order_by('-created_at')[:5]
    recent_leaves = LeaveRequest.objects.select_related('employee', 'leave_type').order_by('-created_at')[:5]
    recent_payslips = Payslip.objects.select_related('employee').order_by('-created_at')[:5]

    context = {
        'total_employees': total_employees,
        'active_employees': active_employees,
        'on_leave_employees': on_leave_employees,
        'departments_count': departments_count,
        'total_payroll_net': total_payroll_net,
        'dept_labels': dept_labels,
        'dept_data': dept_data,
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'rejected_leaves': rejected_leaves,
        'recent_employees': recent_employees,
        'recent_leaves': recent_leaves,
        'recent_payslips': recent_payslips,
    }
    return render(request, 'core/dashboard.html', context)
