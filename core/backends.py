from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from employees.models import Employee


class MultiIdentifierAuthBackend(ModelBackend):
    """
    Authentifie un utilisateur via :
    - son nom d'utilisateur (username)
    - son adresse email (User.email ou Employee.email)
    - son matricule employé (ex: EMP-2026-0001)
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        username = username.strip()
        user = None

        # 1. Recherche par matricule employé
        emp_by_reg = Employee.objects.filter(registration_number__iexact=username, user__isnull=False).select_related('user').first()
        if emp_by_reg and emp_by_reg.user:
            user = emp_by_reg.user

        # 2. Recherche par email employé
        if not user:
            emp_by_email = Employee.objects.filter(email__iexact=username, user__isnull=False).select_related('user').first()
            if emp_by_email and emp_by_email.user:
                user = emp_by_email.user

        # 3. Recherche par User.username ou User.email
        if not user:
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
