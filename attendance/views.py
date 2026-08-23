from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Attendance
from .forms import AttendanceForm
from employees.models import Employee

class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/attendance_list.html'
    context_object_name = 'attendances'
    paginate_by = 15

    def get_queryset(self):
        queryset = Attendance.objects.select_related('employee').all()
        date = self.request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
        status = self.request.GET.get('status')
        
        if date:
            queryset = queryset.filter(date=date)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_date = self.request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
        context['selected_date'] = selected_date
        context['present_count'] = Attendance.objects.filter(date=selected_date, status='PRESENT').count()
        context['late_count'] = Attendance.objects.filter(date=selected_date, status='RETARD').count()
        context['absent_count'] = Attendance.objects.filter(date=selected_date, status='ABSENT').count()
        return context


class AttendanceCreateView(LoginRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'attendance/attendance_form.html'
    success_url = reverse_lazy('attendance_list')

    def form_valid(self, form):
        messages.success(self.request, "Pointage enregistré avec succès.")
        return super().form_valid(form)
