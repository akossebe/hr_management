from django import forms
from .models import Employee, Department, Position

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'manager', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Ressources Humaines'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: RH'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description du département...'}),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'department', 'base_salary_min', 'base_salary_max', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Développeur Full-Stack'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'base_salary_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'base_salary_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'registration_number', 'first_name', 'last_name', 'email', 'phone', 
            'date_of_birth', 'gender', 'marital_status', 'address',
            'emergency_contact_name', 'emergency_contact_phone', 'photo',
            'department', 'position', 'manager', 'contract_type', 'status',
            'hire_date', 'contract_end_date', 'base_salary'
        ]
        widgets = {
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EMP-2026-001'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jean'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dupont'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jean.dupont@entreprise.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+33 6 12 34 56 78'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'contract_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contract_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'base_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '100'}),
        }
