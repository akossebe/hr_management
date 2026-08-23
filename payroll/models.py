from django.db import models
from employees.models import Employee

class Payslip(models.Model):
    MONTH_CHOICES = (
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
    )

    STATUS_CHOICES = (
        ('BROUILLON', 'Brouillon'),
        ('VALIDE', 'Validé'),
        ('PAYE', 'Payé'),
    )

    PAYMENT_METHODS = (
        ('VIREMENT', 'Virement bancaire'),
        ('CHEQUE', 'Chèque'),
        ('ESPECES', 'Espèces'),
    )

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='payslips',
        verbose_name="Employé"
    )
    month = models.IntegerField(choices=MONTH_CHOICES, verbose_name="Mois")
    year = models.IntegerField(default=2026, verbose_name="Année")
    
    basic_salary = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Salaire de base")
    transport_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prime de transport")
    housing_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Indemnité de logement")
    performance_bonus = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Prime de performance")
    
    tax_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Impôt sur le revenu (IRPP)")
    social_security_deduction = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Cotisations sociales (CNSS)")
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Autres déductions")

    gross_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Salaire brut")
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Salaire net à payer")

    payment_date = models.DateField(null=True, blank=True, verbose_name="Date de paiement")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='VIREMENT', verbose_name="Mode de paiement")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='BROUILLON', verbose_name="Statut")
    notes = models.TextField(blank=True, verbose_name="Notes / Remarques")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bulletin de paie"
        verbose_name_plural = "Bulletins de paie"
        unique_together = ('employee', 'month', 'year')
        ordering = ['-year', '-month']

    def __str__(self):
        return f"Bulletin {self.get_month_display()} {self.year} - {self.employee.full_name}"

    def save(self, *args, **kwargs):
        from decimal import Decimal
        self.basic_salary = Decimal(str(self.basic_salary or 0))
        self.transport_allowance = Decimal(str(self.transport_allowance or 0))
        self.housing_allowance = Decimal(str(self.housing_allowance or 0))
        self.performance_bonus = Decimal(str(self.performance_bonus or 0))
        self.tax_deduction = Decimal(str(self.tax_deduction or 0))
        self.social_security_deduction = Decimal(str(self.social_security_deduction or 0))
        self.other_deductions = Decimal(str(self.other_deductions or 0))

        self.gross_salary = (
            self.basic_salary + 
            self.transport_allowance + 
            self.housing_allowance + 
            self.performance_bonus
        )
        total_deductions = (
            self.tax_deduction + 
            self.social_security_deduction + 
            self.other_deductions
        )
        self.net_salary = max(self.gross_salary - total_deductions, Decimal('0.00'))
        super().save(*args, **kwargs)
