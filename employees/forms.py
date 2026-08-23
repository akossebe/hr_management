from django import forms
from django.contrib.auth.models import User
from .models import Employee, Department, Position, EmployeeDocument


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'manager', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Direction Technique'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: DT / IT'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Missions principales du département...'}),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'department', 'base_salary_min', 'base_salary_max', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Ingénieur DevOps'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'base_salary_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ex: 3500'}),
            'base_salary_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ex: 5500'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Responsabilités, compétences requises...'}),
        }


class EmployeeForm(forms.ModelForm):
    # Champs optionnels pour créer le compte utilisateur Django
    create_user_account = forms.BooleanField(
        required=False,
        initial=True,
        label="Créer un compte d'accès web pour ce collaborateur",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    account_password = forms.CharField(
        required=False,
        label="Mot de passe initial",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Laissez vide pour mot de passe par défaut (ex: TempPass2026!)'
        })
    )
    is_admin_user = forms.BooleanField(
        required=False,
        label="Accès Administrateur / RH (Staff)",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Employee
        fields = [
            # Identité & État Civil
            'registration_number', 'first_name', 'last_name', 'gender', 'marital_status',
            'date_of_birth', 'place_of_birth', 'nationality', 'national_id_number', 'blood_group',
            
            # Coordonnées
            'email', 'personal_email', 'phone', 'address', 'city', 'postal_code',
            
            # Contact d'Urgence
            'emergency_contact_name', 'emergency_contact_relation', 'emergency_contact_phone',
            
            # Photo
            'photo',
            
            # Affectation & Contrat
            'department', 'position', 'manager', 'contract_type', 'status',
            'hire_date', 'probation_end_date', 'contract_end_date',
            
            # Rémunération & Banque
            'base_salary', 'bank_name', 'iban', 'swift_bic',
            
            # Compétences & Notes
            'skills', 'notes'
        ]
        widgets = {
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Laisser vide pour génération automatique'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jean'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dupont'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'marital_status': forms.Select(attrs={'class': 'form-select'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paris, Lyon...'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Française'}),
            'national_id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° Sécu / Passeport'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jean.dupont@entreprise.com'}),
            'personal_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'jean.dupont.perso@gmail.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+33 6 12 34 56 78'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': '123 Rue de la Paix'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paris'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '75001'}),
            
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Marie Dupont'}),
            'emergency_contact_relation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Conjointe, Père, Ami...'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+33 6 98 76 54 32'}),
            
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            
            'department': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'contract_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'probation_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contract_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            
            'base_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '100', 'placeholder': 'ex: 4500'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BNP Paribas, Société Générale...'}),
            'iban': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FR76 ...'}),
            'swift_bic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BNPAFRPP'}),
            
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, React, Leadership (séparés par des virgules)'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observations ou remarques RH...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['registration_number'].required = False
        if self.instance and self.instance.pk and self.instance.user:
            self.fields['create_user_account'].initial = True
            self.fields['is_admin_user'].initial = self.instance.user.is_staff


class EmployeeUserAccountForm(forms.Form):
    """Formulaire pour créer ou modifier l'accès utilisateur depuis la fiche détail."""
    username = forms.CharField(
        label="Nom d'utilisateur (Username)",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: jean.dupont'})
    )
    password = forms.CharField(
        label="Nouveau Mot de Passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe sécurisé'}),
        required=False
    )
    is_active = forms.BooleanField(
        label="Compte actif (autoriser la connexion)",
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_staff = forms.BooleanField(
        label="Droits d'administration RH (Staff)",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class EmployeeDocumentForm(forms.ModelForm):
    class Meta:
        model = EmployeeDocument
        fields = ['title', 'document_type', 'file', 'expiry_date', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: Contrat de travail signé'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'required': 'required'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Observations optionnelles...'}),
        }
