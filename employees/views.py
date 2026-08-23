from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Employee, Department, Position
from .forms import EmployeeForm, DepartmentForm, PositionForm

class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        queryset = Employee.objects.select_related('department', 'position', 'manager').all()
        query = self.request.GET.get('q')
        dept_id = self.request.GET.get('department')
        status = self.request.GET.get('status')
        contract = self.request.GET.get('contract_type')

        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(registration_number__icontains=query) |
                Q(email__icontains=query)
            )

        if dept_id:
            queryset = queryset.filter(department_id=dept_id)

        if status:
            queryset = queryset.filter(status=status)

        if contract:
            queryset = queryset.filter(contract_type=contract)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['total_count'] = Employee.objects.count()
        context['active_count'] = Employee.objects.filter(status='ACTIF').count()
        context['leave_count'] = Employee.objects.filter(status='EN_CONGE').count()
        context['selected_dept'] = self.request.GET.get('department', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_contract'] = self.request.GET.get('contract_type', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emp = self.object
        context['recent_leaves'] = emp.leave_requests.all()[:5]
        context['recent_payslips'] = emp.payslips.all()[:5]
        context['recent_attendances'] = emp.attendances.all()[:10]
        context['subordinates'] = emp.subordinates.all()
        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        messages.success(self.request, f"L'employé {form.instance.full_name} a été créé avec succès.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ajouter un nouvel employé"
        context['action'] = "Créer"
        return context


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'

    def form_valid(self, form):
        messages.success(self.request, f"Fiche de {form.instance.full_name} mise à jour avec succès.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Modifier l'employé : {self.object.full_name}"
        context['action'] = "Enregistrer la modification"
        return context


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "L'employé a été supprimé de la base de données.")
        return super().delete(request, *args, **kwargs)


# Department Management Views
class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'employees/department_list.html'
    context_object_name = 'departments'

    def get_queryset(self):
        return Department.objects.annotate(emp_count=Count('employees')).all()


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employees/department_form.html'
    success_url = reverse_lazy('department_list')

    def form_valid(self, form):
        messages.success(self.request, "Département ajouté avec succès.")
        return super().form_valid(form)


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employees/department_form.html'
    success_url = reverse_lazy('department_list')


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'employees/department_confirm_delete.html'
    success_url = reverse_lazy('department_list')
