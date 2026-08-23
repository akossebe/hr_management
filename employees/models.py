from django.db import models
from django.urls import reverse
import uuid

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


class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
        ('O', 'Autre'),
    )

    MARITAL_STATUS_CHOICES = (
        ('CELIBATAIRE', 'Célibataire'),
        ('MARIE', 'Marié(e)'),
        ('DIVORCE', 'Divorcé(e)'),
        ('VEUF', 'Veuf/Veuve'),
    )

    CONTRACT_CHOICES = (
        ('CDI', 'Contrat à Durée Indéterminée (CDI)'),
        ('CDD', 'Contrat à Durée Déterminée (CDD)'),
        ('STAGE', 'Stage'),
        ('FREELANCE', 'Freelance / Prestatation'),
        ('INTERIM', 'Intérim'),
    )

    STATUS_CHOICES = (
        ('ACTIF', 'Actif'),
        ('EN_CONGE', 'En congé'),
        ('SUSPENDU', 'Suspendu'),
        ('DEMISSIONNE', 'Démissionné'),
        ('LICENCIE', 'Licencié'),
    )

    registration_number = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Matricule", 
        help_text="Identifiant unique de l'employé (ex: EMP-2026-001)"
    )
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    email = models.EmailField(unique=True, verbose_name="Adresse Email")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', verbose_name="Genre")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default='CELIBATAIRE', verbose_name="Statut matrimonial")
    address = models.TextField(blank=True, verbose_name="Adresse résidentielle")
    
    emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name="Contact d'urgence (Nom)")
    emergency_contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Contact d'urgence (Tél)")
    
    photo = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Photo de profil")
    
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
    
    contract_type = models.CharField(max_length=20, choices=CONTRACT_CHOICES, default='CDI', verbose_name="Type de contrat")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIF', verbose_name="Statut")
    hire_date = models.DateField(verbose_name="Date d'embauche")
    contract_end_date = models.DateField(null=True, blank=True, verbose_name="Fin de contrat (si applicable)")
    base_salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Salaire de base")
    
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

    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.registration_number:
            import random
            num = random.randint(100, 999)
            self.registration_number = f"EMP-2026-{num}"
        super().save(*args, **kwargs)
