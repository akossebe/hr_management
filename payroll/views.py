from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Payslip
from .forms import PayslipForm

class PayslipListView(LoginRequiredMixin, ListView):
    model = Payslip
    template_name = 'payroll/payslip_list.html'
    context_object_name = 'payslips'
    paginate_by = 10

    def get_queryset(self):
        queryset = Payslip.objects.select_related('employee', 'employee__department').all()
        month = self.request.GET.get('month')
        year = self.request.GET.get('year')
        status = self.request.GET.get('status')

        if month:
            queryset = queryset.filter(month=month)
        if year:
            queryset = queryset.filter(year=year)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context['total_gross'] = qs.aggregate(Sum('gross_salary'))['gross_salary__sum'] or 0
        context['total_net'] = qs.aggregate(Sum('net_salary'))['net_salary__sum'] or 0
        context['total_count'] = qs.count()
        context['selected_month'] = self.request.GET.get('month', '')
        context['selected_year'] = self.request.GET.get('year', '2026')
        return context


class PayslipDetailView(LoginRequiredMixin, DetailView):
    model = Payslip
    template_name = 'payroll/payslip_detail.html'
    context_object_name = 'payslip'


class PayslipCreateView(LoginRequiredMixin, CreateView):
    model = Payslip
    form_class = PayslipForm
    template_name = 'payroll/payslip_form.html'
    success_url = reverse_lazy('payslip_list')

    def form_valid(self, form):
        messages.success(self.request, f"Bulletin de paie généré avec succès pour {form.instance.employee.full_name}.")
        return super().form_valid(form)


class PayslipUpdateView(LoginRequiredMixin, UpdateView):
    model = Payslip
    form_class = PayslipForm
    template_name = 'payroll/payslip_form.html'
    success_url = reverse_lazy('payslip_list')


class PayslipDeleteView(LoginRequiredMixin, DeleteView):
    model = Payslip
    template_name = 'payroll/payslip_confirm_delete.html'
    success_url = reverse_lazy('payslip_list')
