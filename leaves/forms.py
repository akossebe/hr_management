from django import forms
from .models import LeaveRequest, LeaveType

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'leave_type': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Expliquez brièvement le motif du congé...'}),
        }


class LeaveApprovalForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['status', 'hr_comment']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'hr_comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Commentaire de validation ou refus...'}),
        }
