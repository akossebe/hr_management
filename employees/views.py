import csv
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count, Sum, Avg
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Employee, Department, Position, EmployeeDocument
from .forms import EmployeeForm, DepartmentForm, PositionForm, EmployeeDocumentForm, EmployeeUserAccountForm


# ==========================================
# 1. EMPLOYEE VIEWS
# ==========================================

class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = 'employees/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 12

    def get_queryset(self):
        queryset = Employee.objects.select_related('department', 'position', 'manager', 'user').all()
        query = self.request.GET.get('q')
        dept_id = self.request.GET.get('department')
        status = self.request.GET.get('status')
        contract = self.request.GET.get('contract_type')
        gender = self.request.GET.get('gender')
        filter_type = self.request.GET.get('filter')

        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(registration_number__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query) |
                Q(skills__icontains=query)
            )

        if dept_id:
            queryset = queryset.filter(department_id=dept_id)

        if status:
            queryset = queryset.filter(status=status)

        if contract:
            queryset = queryset.filter(contract_type=contract)

        if gender:
            queryset = queryset.filter(gender=gender)

        if filter_type == 'probation':
            queryset = queryset.filter(probation_end_date__gte=date.today())
        elif filter_type == 'expiring':
            from datetime import timedelta
            thirty_days_later = date.today() + timedelta(days=30)
            queryset = queryset.filter(
                contract_end_date__gte=date.today(),
                contract_end_date__lte=thirty_days_later,
                status='ACTIF'
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        from datetime import timedelta
        thirty_days = today + timedelta(days=30)

        context['departments'] = Department.objects.all()
        context['total_count'] = Employee.objects.count()
        context['active_count'] = Employee.objects.filter(status='ACTIF').count()
        context['leave_count'] = Employee.objects.filter(status='EN_CONGE').count()
        context['probation_count'] = Employee.objects.filter(probation_end_date__gte=today).count()
        context['expiring_count'] = Employee.objects.filter(
            contract_end_date__gte=today,
            contract_end_date__lte=thirty_days,
            status='ACTIF'
        ).count()

        # Filters state
        context['selected_dept'] = self.request.GET.get('department', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_contract'] = self.request.GET.get('contract_type', '')
        context['selected_gender'] = self.request.GET.get('gender', '')
        context['selected_filter'] = self.request.GET.get('filter', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['view_mode'] = self.request.GET.get('view', 'table')
        return context


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emp = self.object
        context['documents'] = emp.documents.all()
        context['document_form'] = EmployeeDocumentForm()
        context['recent_leaves'] = emp.leave_requests.all()[:5]
        context['recent_payslips'] = emp.payslips.all()[:5]
        context['recent_attendances'] = emp.attendances.all()[:10]
        context['subordinates'] = emp.subordinates.all()

        # Initialisation du formulaire de gestion de compte utilisateur
        if emp.user:
            context['user_account_form'] = EmployeeUserAccountForm(initial={
                'username': emp.user.username,
                'is_active': emp.user.is_active,
                'is_staff': emp.user.is_staff
            })
        else:
            default_username = emp.email.split('@')[0] if emp.email else f"{emp.first_name.lower()}.{emp.last_name.lower()}"
            context['user_account_form'] = EmployeeUserAccountForm(initial={
                'username': default_username,
                'is_active': True,
                'is_staff': False
            })
        return context


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        employee = self.object

        # Création optionnelle du compte utilisateur Django
        create_account = form.cleaned_data.get('create_user_account')
        if create_account:
            username = employee.email.split('@')[0]
            # S'assurer de l'unicité du username
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            raw_password = form.cleaned_data.get('account_password') or "HRPulse2026!"
            is_admin = form.cleaned_data.get('is_admin_user', False)

            user = User.objects.create_user(
                username=username,
                email=employee.email,
                password=raw_password,
                first_name=employee.first_name,
                last_name=employee.last_name,
                is_staff=is_admin
            )
            employee.user = user
            employee.save()

            messages.success(
                self.request, 
                f"L'employé {employee.full_name} a été créé avec un compte d'accès web ! "
                f"Identifiant : '{username}' | Mot de passe : '{raw_password}'"
            )
        else:
            messages.success(self.request, f"L'employé {employee.full_name} a été ajouté avec succès.")

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Ajouter un nouvel employé"
        context['action'] = "Créer la fiche collaborateur"
        return context


class EmployeeUpdateView(LoginRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/employee_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        employee = self.object
        
        # Mettre à jour l'email et le nom de l'utilisateur associé s'il existe
        if employee.user:
            user = employee.user
            user.email = employee.email
            user.first_name = employee.first_name
            user.last_name = employee.last_name
            if 'is_admin_user' in form.cleaned_data:
                user.is_staff = form.cleaned_data['is_admin_user']
            user.save()

        messages.success(self.request, f"Fiche de {employee.full_name} mise à jour avec succès.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Modifier l'employé : {self.object.full_name}"
        context['action'] = "Enregistrer les modifications"
        return context


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    model = Employee
    template_name = 'employees/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

    def delete(self, request, *args, **kwargs):
        emp = self.get_object()
        user = emp.user
        emp_name = emp.full_name
        response = super().delete(request, *args, **kwargs)
        if user:
            user.delete()
        messages.warning(self.request, f"L'employé {emp_name} et son compte associé ont été supprimés.")
        return response


# ==========================================
# 2. USER ACCOUNT MANAGEMENT (IDENTIFIANTS)
# ==========================================

class EmployeeManageAccountView(LoginRequiredMixin, View):
    """Permet de créer, réinitialiser ou activer/désactiver le compte de connexion d'un employé."""
    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeUserAccountForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']
            is_active = form.cleaned_data['is_active']
            is_staff = form.cleaned_data['is_staff']

            if employee.user:
                # Mise à jour du compte existant
                user = employee.user
                if User.objects.exclude(pk=user.pk).filter(username=username).exists():
                    messages.error(request, f"Le nom d'utilisateur '{username}' est déjà utilisé par un autre compte.")
                    return redirect('employee_detail', pk=pk)
                user.username = username
                user.is_active = is_active
                user.is_staff = is_staff
                if password:
                    user.set_password(password)
                    messages.success(request, f"Compte mis à jour ! Nouveau mot de passe défini pour {username} : '{password}'")
                else:
                    messages.success(request, f"Paramètres du compte {username} mis à jour avec succès.")
                user.save()
            else:
                # Création d'un nouveau compte
                if User.objects.filter(username=username).exists():
                    messages.error(request, f"Le nom d'utilisateur '{username}' existe déjà. Veuillez en choisir un autre.")
                    return redirect('employee_detail', pk=pk)
                
                raw_password = password if password else "HRPulse2026!"
                user = User.objects.create_user(
                    username=username,
                    email=employee.email,
                    password=raw_password,
                    first_name=employee.first_name,
                    last_name=employee.last_name,
                    is_active=is_active,
                    is_staff=is_staff
                )
                employee.user = user
                employee.save()
                messages.success(
                    request, 
                    f"Compte d'accès créé avec succès pour {employee.full_name} ! "
                    f"Identifiant : '{username}' (ou email: '{employee.email}') | Mot de passe : '{raw_password}'"
                )
        else:
            messages.error(request, "Données invalides dans le formulaire de compte.")

        return redirect('employee_detail', pk=pk)


# ==========================================
# 3. DOCUMENT MANAGEMENT VIEWS
# ==========================================

class EmployeeDocumentUploadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        form = EmployeeDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.employee = employee
            doc.save()
            messages.success(request, f"Le document '{doc.title}' a été ajouté avec succès.")
        else:
            messages.error(request, "Erreur lors du téléversement du document. Veuillez vérifier le fichier.")
        return redirect('employee_detail', pk=pk)


class EmployeeDocumentDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk, doc_pk):
        employee = get_object_or_404(Employee, pk=pk)
        doc = get_object_or_404(EmployeeDocument, pk=doc_pk, employee=employee)
        doc_title = doc.title
        doc.delete()
        messages.info(request, f"Le document '{doc_title}' a été supprimé.")
        return redirect('employee_detail', pk=pk)


# ==========================================
# 4. EXPORTS & BADGE
# ==========================================

class EmployeeBadgeView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = 'employees/employee_badge.html'
    context_object_name = 'employee'


def export_employees_csv(request):
    """Exporte la liste des employés au format CSV (UTF-8 avec BOM pour Excel)."""
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = f'attachment; filename="liste_employes_{date.today().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Matricule', 'Prénom', 'Nom', 'Email Pro', 'Téléphone', 'Genre', 'Statut Matrimonial',
        'Date de Naissance', 'Département', 'Poste', 'Manager', 'Type Contrat',
        'Statut', 'Date Embauche', 'Fin Contrat', 'Salaire de Base', 'Banque', 'IBAN'
    ])

    employees = Employee.objects.select_related('department', 'position', 'manager').all()
    
    dept_id = request.GET.get('department')
    status = request.GET.get('status')
    contract = request.GET.get('contract_type')
    if dept_id:
        employees = employees.filter(department_id=dept_id)
    if status:
        employees = employees.filter(status=status)
    if contract:
        employees = employees.filter(contract_type=contract)

    for emp in employees:
        writer.writerow([
            emp.registration_number,
            emp.first_name,
            emp.last_name,
            emp.email,
            emp.phone,
            emp.get_gender_display(),
            emp.get_marital_status_display(),
            emp.date_of_birth.strftime('%d/%m/%Y') if emp.date_of_birth else '',
            emp.department.name if emp.department else '',
            emp.position.title if emp.position else '',
            emp.manager.full_name if emp.manager else '',
            emp.get_contract_type_display(),
            emp.get_status_display(),
            emp.hire_date.strftime('%d/%m/%Y') if emp.hire_date else '',
            emp.contract_end_date.strftime('%d/%m/%Y') if emp.contract_end_date else '',
            f"{emp.base_salary:.2f}",
            emp.bank_name,
            emp.iban,
        ])

    return response


# ==========================================
# 5. ORGANIGRAMME (ORG CHART)
# ==========================================

class OrgChartView(LoginRequiredMixin, TemplateView):
    template_name = 'employees/org_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        departments = Department.objects.prefetch_related('employees__position', 'employees__manager').all()
        
        top_managers = Employee.objects.filter(
            status='ACTIF',
            subordinates__isnull=False
        ).distinct()

        context['departments'] = departments
        context['top_managers'] = top_managers
        context['total_employees'] = Employee.objects.filter(status='ACTIF').count()
        return context


# ==========================================
# 6. DEPARTMENT MANAGEMENT VIEWS
# ==========================================

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'employees/department_list.html'
    context_object_name = 'departments'

    def get_queryset(self):
        return Department.objects.annotate(
            emp_count=Count('employees'),
            total_salary=Sum('employees__base_salary')
        ).all()


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    template_name = 'employees/department_detail.html'
    context_object_name = 'department'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dept = self.object
        employees = dept.employees.select_related('position').all()
        context['employees'] = employees
        context['positions'] = dept.positions.annotate(emp_count=Count('employees')).all()
        context['total_payroll'] = employees.aggregate(total=Sum('base_salary'))['total'] or 0
        context['avg_salary'] = employees.aggregate(avg=Avg('base_salary'))['avg'] or 0
        context['active_count'] = employees.filter(status='ACTIF').count()
        return context


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employees/department_form.html'
    success_url = reverse_lazy('department_list')

    def form_valid(self, form):
        messages.success(self.request, f"Le département {form.instance.name} a été créé.")
        return super().form_valid(form)


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'employees/department_form.html'
    success_url = reverse_lazy('department_list')

    def form_valid(self, form):
        messages.success(self.request, f"Département {form.instance.name} mis à jour avec succès.")
        return super().form_valid(form)


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'employees/department_confirm_delete.html'
    success_url = reverse_lazy('department_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, f"Le département {self.get_object().name} a été supprimé.")
        return super().delete(request, *args, **kwargs)


# ==========================================
# 7. POSITION MANAGEMENT VIEWS (POSTES)
# ==========================================

class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    template_name = 'employees/position_list.html'
    context_object_name = 'positions'

    def get_queryset(self):
        queryset = Position.objects.select_related('department').annotate(
            emp_count=Count('employees')
        ).all()
        dept_id = self.request.GET.get('department')
        if dept_id:
            queryset = queryset.filter(department_id=dept_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = Department.objects.all()
        context['selected_dept'] = self.request.GET.get('department', '')
        return context


class PositionCreateView(LoginRequiredMixin, CreateView):
    model = Position
    form_class = PositionForm
    template_name = 'employees/position_form.html'
    success_url = reverse_lazy('position_list')

    def form_valid(self, form):
        messages.success(self.request, f"Le poste '{form.instance.title}' a été créé avec succès.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Créer un nouveau poste"
        context['action'] = "Créer le poste"
        return context


class PositionUpdateView(LoginRequiredMixin, UpdateView):
    model = Position
    form_class = PositionForm
    template_name = 'employees/position_form.html'
    success_url = reverse_lazy('position_list')

    def form_valid(self, form):
        messages.success(self.request, f"Le poste '{form.instance.title}' a été modifié avec succès.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Modifier le poste : {self.object.title}"
        context['action'] = "Enregistrer"
        return context


class PositionDeleteView(LoginRequiredMixin, DeleteView):
    model = Position
    template_name = 'employees/position_confirm_delete.html'
    success_url = reverse_lazy('position_list')

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, f"Le poste '{self.get_object().title}' a été supprimé.")
        return super().delete(request, *args, **kwargs)
