from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from employees.models import Employee, Department
from leaves.models import LeaveRequest, LeaveType
from payroll.models import Payslip
from attendance.models import Attendance


class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True


@login_required
def dashboard_view(request):
    # Si c'est un employé sans droits d'administration, on le redirige vers son Espace Collaborateur
    if not request.user.is_staff and not request.user.is_superuser and hasattr(request.user, 'employee_profile'):
        return redirect('employee_portal')

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


@login_required
def employee_portal_view(request):
    """Espace personnel (Self-Service) pour le collaborateur connecté."""
    # Récupérer le profil employé de l'utilisateur connecté
    employee = getattr(request.user, 'employee_profile', None)
    
    if not employee:
        if request.user.is_staff or request.user.is_superuser:
            # Si c'est un admin sans profil employé direct, on lui montre le premier employé pour prévisualiser ou on redirige
            first_emp = Employee.objects.first()
            if first_emp:
                employee = first_emp
            else:
                messages.info(request, "Aucun profil employé n'est lié à votre compte admin.")
                return redirect('dashboard')
        else:
            messages.error(request, "Aucun profil collaborateur n'est associé à ce compte utilisateur.")
            return redirect('login')

    today = date.today()
    # Pointage d'aujourd'hui
    today_attendance = Attendance.objects.filter(employee=employee, date=today).first()
    
    # Demandes de congés du collaborateur
    my_leaves = LeaveRequest.objects.filter(employee=employee).select_related('leave_type').order_by('-created_at')[:5]
    pending_leaves_count = LeaveRequest.objects.filter(employee=employee, status='EN_ATTENTE').count()
    
    # Bulletins de paie du collaborateur
    my_payslips = Payslip.objects.filter(employee=employee).order_by('-year', '-month')[:6]
    
    # Documents
    my_documents = employee.documents.all()[:5]

    context = {
        'employee': employee,
        'today': today,
        'today_attendance': today_attendance,
        'my_leaves': my_leaves,
        'pending_leaves_count': pending_leaves_count,
        'my_payslips': my_payslips,
        'my_documents': my_documents,
    }
    return render(request, 'core/employee_portal.html', context)


@login_required
def quick_attendance_punch(request):
    """Permet au collaborateur de pointer son arrivée ou son départ en 1 clic."""
    if request.method == 'POST':
        employee = getattr(request.user, 'employee_profile', None)
        if not employee:
            messages.error(request, "Impossible de pointer : aucun profil employé rattaché.")
            return redirect('employee_portal')

        today = date.today()
        now_time = timezone.now().time().strftime('%H:%M:%S')

        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={
                'time_in': now_time,
                'status': 'PRESENT',
                'notes': 'Pointage portail web'
            }
        )

        if not created:
            # Si le pointage existe déjà et qu'il n'a pas encore de time_out, on enregistre l'heure de départ
            if not attendance.time_out:
                attendance.time_out = now_time
                attendance.save()
                messages.success(request, f"Départ enregistré à {now_time[:5]} pour aujourd'hui.")
            else:
                messages.info(request, "Vos heures d'arrivée et de départ pour aujourd'hui sont déjà enregistrées.")
        else:
            messages.success(request, f"Arrivée enregistrée à {now_time[:5]} ! Bonne journée de travail.")

    return redirect('employee_portal')
