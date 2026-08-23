from django.db import models
from django.utils import timezone
from employees.models import Employee

class LeaveType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Type de congé")
    days_allowed = models.IntegerField(default=25, verbose_name="Jours alloués / an")
    is_paid = models.BooleanField(default=True, verbose_name="Congé payé")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Type de congé"
        verbose_name_plural = "Types de congé"

    def __str__(self):
        return self.name


class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVE', 'Approuvé'),
        ('REFUSE', 'Refusé'),
        ('ANNULE', 'Annulé'),
    )

    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='leave_requests',
        verbose_name="Employé"
    )
    leave_type = models.ForeignKey(
        LeaveType, 
        on_delete=models.CASCADE, 
        related_name='requests',
        verbose_name="Type de congé"
    )
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    reason = models.TextField(verbose_name="Motif / Justificatif")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EN_ATTENTE', verbose_name="Statut")
    hr_comment = models.TextField(blank=True, verbose_name="Commentaire RH / Manager")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de demande")

    class Meta:
        verbose_name = "Demande de congé"
        verbose_name_plural = "Demandes de congé"
        ordering = ['-created_at']

    def __str__(self):
        return f"Congé {self.employee.full_name} ({self.start_date} au {self.end_date})"

    @property
    def duration_days(self):
        if self.start_date and self.end_date:
            delta = (self.end_date - self.start_date).days + 1
            return max(delta, 1)
        return 0
