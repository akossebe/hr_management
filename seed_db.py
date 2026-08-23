import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_config.settings')
django.setup()

from django.contrib.auth.models import User
from employees.models import Department, Position, Employee
from leaves.models import LeaveType, LeaveRequest
from payroll.models import Payslip
from attendance.models import Attendance

def seed():
    print("🌱 Demarrage du remplissage de la base de donnees HR Pulse...")

    # 1. User Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@hrpulse.com', 'admin123')
        print("✅ Superutilisateur cree: identifiant 'admin' / mot de passe 'admin123'")

    # 2. Departments
    departments_data = [
        ('Ressources Humaines', 'RH', 'Gestion des talents, paie et recrutement'),
        ('Ingénierie & IT', 'IT', 'Développement informatique et infrastructure cloud'),
        ('Finance & Comptabilité', 'FIN', 'Gestion financière, budget et audit'),
        ('Marketing & Com', 'MKT', 'Stratégie de marque et communication digitale'),
        ('Ventes & Commercial', 'SALES', 'Développement des affaires et relation client'),
    ]

    depts = {}
    for name, code, desc in departments_data:
        dept, created = Department.objects.get_or_create(code=code, defaults={'name': name, 'description': desc})
        depts[code] = dept
        if created:
            print(f"✅ Département créé: {name}")

    # 3. Positions
    positions_data = [
        ('Directeur RH', 'RH', 4500, 6500),
        ('Chargé de Recrutement', 'RH', 2800, 3800),
        ('Lead Developer Full-Stack', 'IT', 4200, 5800),
        ('Ingénieur DevOps', 'IT', 3900, 5200),
        ('Développeur Python/Django', 'IT', 3200, 4500),
        ('Responsable Financier', 'FIN', 4000, 5500),
        ('Comptable Senior', 'FIN', 2900, 3900),
        ('Growth Marketer', 'MKT', 3000, 4200),
        ('Business Developer', 'SALES', 3100, 5000),
    ]

    positions = []
    for title, dept_code, min_s, max_s in positions_data:
        pos, created = Position.objects.get_or_create(
            title=title, 
            department=depts[dept_code], 
            defaults={'base_salary_min': min_s, 'base_salary_max': max_s}
        )
        positions.append(pos)
        if created:
            print(f"✅ Poste créé: {title}")

    # 4. Employees
    employees_data = [
        ('EMP-2026-001', 'Sophie', 'Martin', 'sophie.martin@hrpulse.com', '+33 6 12 34 56 78', 'F', 'MARIE', 'RH', 'Directeur RH', 'CDI', 5200, '2021-03-15'),
        ('EMP-2026-002', 'Alexandre', 'Dubois', 'alex.dubois@hrpulse.com', '+33 6 98 76 54 32', 'M', 'CELIBATAIRE', 'IT', 'Lead Developer Full-Stack', 'CDI', 4800, '2022-01-10'),
        ('EMP-2026-003', 'Camille', 'Leroy', 'camille.leroy@hrpulse.com', '+33 6 55 44 33 22', 'F', 'CELIBATAIRE', 'IT', 'Développeur Python/Django', 'CDI', 3500, '2023-06-01'),
        ('EMP-2026-004', 'Lucas', 'Moreau', 'lucas.moreau@hrpulse.com', '+33 6 11 22 33 44', 'M', 'MARIE', 'FIN', 'Responsable Financier', 'CDI', 4500, '2020-09-01'),
        ('EMP-2026-005', 'Emma', 'Bernard', 'emma.bernard@hrpulse.com', '+33 6 77 88 99 00', 'F', 'CELIBATAIRE', 'MKT', 'Growth Marketer', 'CDD', 3200, '2024-02-15'),
        ('EMP-2026-006', 'Antoine', 'Rousseau', 'antoine.rousseau@hrpulse.com', '+33 6 33 22 11 00', 'M', 'CELIBATAIRE', 'SALES', 'Business Developer', 'CDI', 3400, '2023-11-01'),
    ]

    employees = []
    for reg, fn, ln, email, phone, gender, marital, dept_code, pos_title, contract, salary, hire_date in employees_data:
        pos_obj = Position.objects.filter(title=pos_title).first()
        emp, created = Employee.objects.get_or_create(
            registration_number=reg,
            defaults={
                'first_name': fn,
                'last_name': ln,
                'email': email,
                'phone': phone,
                'gender': gender,
                'marital_status': marital,
                'department': depts[dept_code],
                'position': pos_obj,
                'contract_type': contract,
                'status': 'ACTIF',
                'hire_date': hire_date,
                'base_salary': salary,
                'address': '15 Rue de la Paix, 75002 Paris',
                'emergency_contact_name': 'Parent / Conjoint',
                'emergency_contact_phone': '+33 6 00 00 00 00'
            }
        )
        employees.append(emp)
        if created:
            print(f"👤 Employé créé: {emp.full_name} ({reg})")

    # Set manager for department
    rh_manager = Employee.objects.filter(registration_number='EMP-2026-001').first()
    if rh_manager and depts['RH']:
        depts['RH'].manager = rh_manager
        depts['RH'].save()

    # 5. Leave Types
    leave_types_data = [
        ('Congé Annuel Payé', 25, True),
        ('Maladie / Médical', 10, True),
        ('Maternité / Paternité', 30, True),
        ('Sans Solde', 0, False),
    ]

    l_types = []
    for lt_name, days, is_p in leave_types_data:
        lt, _ = LeaveType.objects.get_or_create(name=lt_name, defaults={'days_allowed': days, 'is_paid': is_p})
        l_types.append(lt)

    # 6. Leave Requests
    if employees and l_types:
        LeaveRequest.objects.get_or_create(
            employee=employees[2],
            start_date=date(2026, 8, 15),
            end_date=date(2026, 8, 22),
            defaults={
                'leave_type': l_types[0],
                'reason': 'Vacances d\'été annuelles',
                'status': 'APPROUVE'
            }
        )
        LeaveRequest.objects.get_or_create(
            employee=employees[4],
            start_date=date(2026, 8, 20),
            end_date=date(2026, 8, 25),
            defaults={
                'leave_type': l_types[0],
                'reason': 'Repos et convenances personnelles',
                'status': 'EN_ATTENTE'
            }
        )
        print("🌴 Demandes de congé d'exemple insérées.")

    # 7. Payslips
    for emp in employees:
        Payslip.objects.get_or_create(
            employee=emp,
            month=8,
            year=2026,
            defaults={
                'basic_salary': emp.base_salary,
                'transport_allowance': 150,
                'housing_allowance': 200 if emp.base_salary > 4000 else 100,
                'performance_bonus': 300 if emp.contract_type == 'CDI' else 0,
                'tax_deduction': round(float(emp.base_salary) * 0.12, 2),
                'social_security_deduction': round(float(emp.base_salary) * 0.08, 2),
                'other_deductions': 0,
                'payment_date': date(2026, 8, 30),
                'payment_method': 'VIREMENT',
                'status': 'VALIDE'
            }
        )
    print("💰 Bulletins de paie d'exemple générés.")

    # 8. Attendance Records
    today = date.today()
    for emp in employees:
        Attendance.objects.get_or_create(
            employee=emp,
            date=today,
            defaults={
                'time_in': '08:45:00' if random.random() > 0.3 else '09:15:00',
                'time_out': '17:30:00',
                'status': 'PRESENT' if random.random() > 0.2 else 'RETARD',
                'notes': 'Pointage automatique badge'
            }
        )
    print("⏰ Pointages du jour générés.")
    print("🎉 Base de données initialisée avec succès !")

if __name__ == '__main__':
    seed()
