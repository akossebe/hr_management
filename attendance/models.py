from django.db import models
from employees.models import Employee

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('PRESENT', 'Présent'),
        ('RETARD', 'En retard'),
        ('ABSENT', 'Absent'),
        ('DEMI_JOURNEE', 'Demi-journée'),
        ('CONGE', 'En congé'),
    )

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='attendances',
        verbose_name="Employé"
    )
    date = models.DateField(verbose_name="Date")
    time_in = models.TimeField(null=True, blank=True, verbose_name="Heure d'arrivée")
    time_out = models.TimeField(null=True, blank=True, verbose_name="Heure de départ")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PRESENT', verbose_name="Statut")
    notes = models.CharField(max_length=255, blank=True, verbose_name="Observations")

    class Meta:
        verbose_name = "Pointage / Présence"
        verbose_name_plural = "Pointages & Présences"
        unique_together = ('employee', 'date')
        ordering = ['-date', 'employee']

    def __str__(self):
        return f"{self.employee.full_name} - {self.date} ({self.get_status_display()})"
