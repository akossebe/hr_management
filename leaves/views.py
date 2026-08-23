from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import LeaveRequest, LeaveType
from .forms import LeaveRequestForm, LeaveApprovalForm

class LeaveListView(LoginRequiredMixin, ListView):
    model = LeaveRequest
    template_name = 'leaves/leave_list.html'
    context_object_name = 'leaves'
    paginate_by = 10

    def get_queryset(self):
        queryset = LeaveRequest.objects.select_related('employee', 'leave_type').all()
        status = self.request.GET.get('status')
        emp_id = self.request.GET.get('employee')
        
        if status:
            queryset = queryset.filter(status=status)
        if emp_id:
            queryset = queryset.filter(employee_id=emp_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_count'] = LeaveRequest.objects.filter(status='EN_ATTENTE').count()
        context['approved_count'] = LeaveRequest.objects.filter(status='APPROUVE').count()
        context['rejected_count'] = LeaveRequest.objects.filter(status='REFUSE').count()
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = LeaveRequest
    form_class = LeaveRequestForm
    template_name = 'leaves/leave_form.html'
    success_url = reverse_lazy('leave_list')

    def form_valid(self, form):
        messages.success(self.request, "Demande de congé enregistrée avec succès.")
        return super().form_valid(form)


class LeaveUpdateStatusView(LoginRequiredMixin, UpdateView):
    model = LeaveRequest
    form_class = LeaveApprovalForm
    template_name = 'leaves/leave_approve.html'
    success_url = reverse_lazy('leave_list')

    def form_valid(self, form):
        req = form.instance
        if req.status == 'APPROUVE':
            # Optionnel: mettre à jour le statut de l'employé
            emp = req.employee
            emp.status = 'EN_CONGE'
            emp.save()
            messages.success(self.request, f"La demande de congé de {emp.full_name} a été APPROUVÉE.")
        elif req.status == 'REFUSE':
            messages.info(self.request, f"La demande de congé de {req.employee.full_name} a été REFUSÉE.")
        return super().form_valid(form)
