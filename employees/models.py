from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import date
import os


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du département")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code département")
    description = models.TextField(blank=True, verbose_name="Description")
    manager = models.ForeignKey(
        'Employee', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='managed_departments',
        verbose_name="Responsable de département"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def employee_count(self):
        return self.employees.count()

    def get_absolute_url(self):
        return reverse('department_detail', kwargs={'pk': self.pk})

    @property
    def total_payroll(self):
        return self.employees.aggregate(total=models.Sum('base_salary'))['total'] or 0


class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name="Intitulé du poste")
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE, 
        related_name='positions',
        verbose_name="Département"
    )
    base_salary_min = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Salaire min (FCFA/€)")
    base_salary_max = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Salaire max (FCFA/€)")
    description = models.TextField(blank=True, verbose_name="Missions et responsabilités")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Poste"
        verbose_name_plural = "Postes"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} - {self.department.name}"

    def employee_count(self):
        return self.employees.count()


class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('O', 'Autre'),
    )

    MARITAL_STATUS_CHOICES = (
        ('CELIBATAIRE', 'Célibataire'),
        ('MARIE', 'Marié(e)'),
        ('PACSE', 'Pacsé(e)'),
        ('DIVORCE', 'Divorcé(e)'),
        ('VEUF', 'Veuf/Veuve'),
    )

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('INCONNU', 'Non renseigné'),
    )

    CONTRACT_CHOICES = (
        ('CDI', 'Contrat à Durée Indéterminée (CDI)'),
        ('CDD', 'Contrat à Durée Déterminée (CDD)'),
        ('STAGE', 'Stage conventionné'),
        ('APPRENTISSAGE', 'Contrat d\'apprentissage / Alternance'),
        ('FREELANCE', 'Freelance / Prestation externe'),
        ('INTERIM', 'Intérim'),
    )

    STATUS_CHOICES = (
        ('ACTIF', 'Actif'),
        ('EN_CONGE', 'En congé'),
        ('EN_FORMATION', 'En formation'),
        ('SUSPENDU', 'Suspendu'),
        ('DEMISSIONNE', 'Démissionné'),
        ('LICENCIE', 'Licencié'),
        ('RETRAITE', 'Retraité'),
    )

    # 1. Identité & État Civil
    registration_number = models.CharField(
        max_length=30, 
        unique=True, 
        verbose_name="Matricule", 
        help_text="Identifiant unique (généré automatiquement si vide)"
    )
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    email = models.EmailField(unique=True, verbose_name="Adresse Email Professionnelle")
    personal_email = models.EmailField(blank=True, verbose_name="Adresse Email Personnelle")
    phone = models.CharField(max_length=25, verbose_name="Téléphone")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    place_of_birth = models.CharField(max_length=100, blank=True, verbose_name="Lieu de naissance")
    nationality = models.CharField(max_length=50, default="Française", verbose_name="Nationalité")
    national_id_number = models.CharField(max_length=50, blank=True, verbose_name="N° CNI / Passeport / Sécurité Sociale")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name="Genre")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='CELIBATAIRE', verbose_name="Statut matrimonial")
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, default='INCONNU', verbose_name="Groupe sanguin")
    address = models.TextField(blank=True, verbose_name="Adresse résidentielle")
    city = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Code postal")
    
    # 2. Contact d'Urgence
    emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name="Contact d'urgence (Nom)")
    emergency_contact_relation = models.CharField(max_length=50, blank=True, verbose_name="Lien de parenté / Relation")
    emergency_contact_phone = models.CharField(max_length=25, blank=True, verbose_name="Contact d'urgence (Tél)")
    
    # 3. Photo & Documents
    photo = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Photo de profil")
    
    # 4. Affectation & Hiérarchie
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='employees',
        verbose_name="Département"
    )
    position = models.ForeignKey(
        Position, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='employees',
        verbose_name="Poste / Fonction"
    )
    manager = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='subordinates',
        verbose_name="Superviseur Hiérarchique"
    )
    
    # 5. Contrat & Temps de Travail
    contract_type = models.CharField(max_length=20, choices=CONTRACT_CHOICES, default='CDI', verbose_name="Type de contrat")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIF', verbose_name="Statut")
    hire_date = models.DateField(verbose_name="Date d'embauche")
    probation_end_date = models.DateField(null=True, blank=True, verbose_name="Fin période d'essai")
    contract_end_date = models.DateField(null=True, blank=True, verbose_name="Fin de contrat (si CDD/Stage)")
    
    # 6. Rémunération & Coordonnées Bancaires
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Salaire de base")
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Nom de la banque")
    iban = models.CharField(max_length=40, blank=True, verbose_name="IBAN / Numéro de compte")
    swift_bic = models.CharField(max_length=20, blank=True, verbose_name="Code SWIFT / BIC")

    # 7. Compétences & Notes
    skills = models.CharField(max_length=255, blank=True, verbose_name="Compétences clés", help_text="Ex: Python, Django, Leadership, Recrutement (séparés par des virgules)")
    notes = models.TextField(blank=True, verbose_name="Notes administratives RH")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.registration_number} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    @property
    def seniority_years(self):
        if self.hire_date:
            today = date.today()
            diff_days = (today - self.hire_date).days
            return round(diff_days / 365.25, 1)
        return 0

    @property
    def seniority_display(self):
        if not self.hire_date:
            return "Non définie"
        today = date.today()
        total_months = (today.year - self.hire_date.year) * 12 + (today.month - self.hire_date.month)
        if today.day < self.hire_date.day:
            total_months -= 1
        
        if total_months < 0:
            return "Embauche future"
        
        years = total_months // 12
        months = total_months % 12
        
        if years == 0 and months == 0:
            return "< 1 mois"
        elif years == 0:
            return f"{months} mois"
        elif months == 0:
            return f"{years} an{'s' if years > 1 else ''}"
        else:
            return f"{years} an{'s' if years > 1 else ''} {months} m"

    @property
    def is_probation_active(self):
        if self.probation_end_date:
            return self.probation_end_date >= date.today()
        return False

    @property
    def is_contract_expiring_soon(self):
        if self.contract_end_date and self.status == 'ACTIF':
            days_left = (self.contract_end_date - date.today()).days
            return 0 <= days_left <= 30
        return False

    @property
    def skill_list(self):
        if self.skills:
            return [s.strip() for s in self.skills.split(',') if s.strip()]
        return []

    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.registration_number:
            year = timezone.now().year
            last_emp = Employee.objects.filter(registration_number__startswith=f"EMP-{year}-").order_by('registration_number').last()
            if last_emp and '-' in last_emp.registration_number:
                try:
                    last_seq = int(last_emp.registration_number.split('-')[-1])
                    seq = last_seq + 1
                except (ValueError, IndexError):
                    seq = Employee.objects.count() + 1
            else:
                seq = Employee.objects.count() + 1
            self.registration_number = f"EMP-{year}-{seq:04d}"
        super().save(*args, **kwargs)


def employee_document_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    safe_title = "".join(c for c in instance.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    return f"documents/employees/{instance.employee.registration_number}/{safe_title}_{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}"


class EmployeeDocument(models.Model):
    DOCUMENT_TYPES = (
        ('CONTRAT', 'Contrat de travail'),
        ('AVENANT', 'Avenant au contrat'),
        ('CNI_PASSEPORT', 'Pièce d\'identité / Passeport'),
        ('CV', 'Curriculum Vitae (CV)'),
        ('DIPLOME', 'Diplôme / Certification'),
        ('VISITE_MEDICALE', 'Certificat visite médicale'),
        ('EVALUATION', 'Fiche d\'évaluation / Entretien'),
        ('RIB', 'Relevé d\'Identité Bancaire (RIB)'),
        ('AUTRE', 'Autre document RH'),
    )

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='documents', 
        verbose_name="Employé"
    )
    title = models.CharField(max_length=150, verbose_name="Intitulé du document")
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES, default='AUTRE', verbose_name="Type de document")
    file = models.FileField(upload_to=employee_document_upload_path, verbose_name="Fichier")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="Date d'expiration (si applicable)")
    notes = models.TextField(blank=True, verbose_name="Observations")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de téléversement")

    class Meta:
        verbose_name = "Document employé"
        verbose_name_plural = "Documents employés"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} ({self.employee.full_name})"

    @property
    def file_extension(self):
        if self.file:
            return os.path.splitext(self.file.name)[1].lower().replace('.', '')
        return ''

    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < date.today()
        return False
