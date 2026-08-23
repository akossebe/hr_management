from django import forms
from .models import Payslip

class PayslipForm(forms.ModelForm):
    class Meta:
        model = Payslip
        fields = [
            'employee', 'month', 'year', 'basic_salary', 
            'transport_allowance', 'housing_allowance', 'performance_bonus',
            'tax_deduction', 'social_security_deduction', 'other_deductions',
            'payment_date', 'payment_method', 'status', 'notes'
        ]
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'month': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '100'}),
            'transport_allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '100'}),
            'housing_allowance': forms.NumberInput(attrs={'class': 'form-control', 'step': '100'}),
            'performance_bonus': forms.NumberInput(attrs={'class': 'form-control', 'step': '100'}),
            'tax_deduction': forms.NumberInput(attrs={'class': 'form-control', 'step': '100'}),
            'social_security_deduction': forms.NumberInput(attrs={'class': 'form-control', 'step': '100'}),
            'other_deductions': forms.NumberInput(attrs={'class': 'form-control', 'step': '100'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
