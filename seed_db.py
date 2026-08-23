import os
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_config.settings')
django.setup()

from django.contrib.auth.models import User
from employees.models import Department, Position, Employee, EmployeeDocument
from leaves.models import LeaveType, LeaveRequest
from payroll.models import Payslip
from attendance.models import Attendance

def seed():
    print("🌱 Démarrage du remplissage de la base de données HR Pulse...")

    # 1. User Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@hrpulse.com', 'admin123')
        print("✅ Superutilisateur créé: identifiant 'admin' / mot de passe 'admin123'")

    # 2. Departments
    departments_data = [
        ('Ressources Humaines', 'RH', 'Gestion des talents, paie, recrutement et relations sociales'),
        ('Ingénierie & IT', 'IT', 'Développement informatique, infrastructure cloud et cybersécurité'),
        ('Finance & Comptabilité', 'FIN', 'Gestion financière, trésorerie, budget et audit'),
        ('Marketing & Communication', 'MKT', 'Stratégie de marque, acquisition et communication digitale'),
        ('Ventes & Commercial', 'SALES', 'Développement des affaires, partenariats et relation client'),
    ]

    depts = {}
    for name, code, desc in departments_data:
        dept, created = Department.objects.get_or_create(code=code, defaults={'name': name, 'description': desc})
        depts[code] = dept
        if created:
            print(f"✅ Département créé: {name}")

    # 3. Positions
    positions_data = [
        ('Directeur RH', 'RH', 4500, 6500, 'Pilotage de la politique RH et relations sociales'),
        ('Chargé de Recrutement', 'RH', 2800, 3800, 'Sourcing, entretiens et onboarding des nouveaux talents'),
        ('Lead Developer Full-Stack', 'IT', 4200, 5800, 'Architecture logicielle, lead technique et mentorat'),
        ('Ingénieur DevOps & Cloud', 'IT', 3900, 5200, 'Gestion CI/CD, conteneurs et infrastructure AWS/GCP'),
        ('Développeur Python / Django', 'IT', 3200, 4500, 'Conception et maintenance des applications web'),
        ('Responsable Financier', 'FIN', 4000, 5500, 'Clôture comptable, budgets et reporting financier'),
        ('Comptable Senior', 'FIN', 2900, 3900, 'Tenue des comptes, déclarations fiscales et sociales'),
        ('Growth Marketer & SEO', 'MKT', 3000, 4200, 'Campagnes d\'acquisition, analytics et SEO'),
        ('Business Developer B2B', 'SALES', 3100, 5000, 'Prospection commerciale et négociation de contrats'),
    ]

    positions = {}
    for title, dept_code, min_s, max_s, desc in positions_data:
        pos, created = Position.objects.get_or_create(
            title=title, 
            department=depts[dept_code], 
            defaults={'base_salary_min': min_s, 'base_salary_max': max_s, 'description': desc}
        )
        positions[title] = pos
        if created:
            print(f"✅ Poste créé: {title}")

    # 4. Employees
    employees_data = [
        (
            'EMP-2026-0001', 'Sophie', 'Martin', 'sophie.martin@hrpulse.com', '+33 6 12 34 56 78',
            'F', 'MARIE', 'RH', 'Directeur RH', 'CDI', 5200, date(2021, 3, 15), None, None,
            'Recrutement, Droit du travail, Paie, Négociation', 'BNP Paribas', 'FR76 3000 4000 5000 1234 5678 901',
            'Claire Martin', 'Sœur', '+33 6 11 22 33 44', 'O+'
        ),
        (
            'EMP-2026-0002', 'Alexandre', 'Dubois', 'alex.dubois@hrpulse.com', '+33 6 98 76 54 32',
            'M', 'CELIBATAIRE', 'IT', 'Lead Developer Full-Stack', 'CDI', 4800, date(2022, 1, 10), None, None,
            'Python, Django, React, PostgreSQL, Docker, Architecture', 'Société Générale', 'FR76 3000 3000 2000 9876 5432 100',
            'Marc Dubois', 'Père', '+33 6 99 88 77 66', 'A+'
        ),
        (
            'EMP-2026-0003', 'Camille', 'Leroy', 'camille.leroy@hrpulse.com', '+33 6 55 44 33 22',
            'F', 'CELIBATAIRE', 'IT', 'Développeur Python / Django', 'CDI', 3500, date(2023, 6, 1), None, None,
            'Python, Django REST Framework, Vue.js, Git, Celery', 'Crédit Agricole', 'FR76 1820 6000 1000 4455 6677 889',
            'Lucie Leroy', 'Mère', '+33 6 55 11 22 33', 'B+'
        ),
        (
            'EMP-2026-0004', 'Lucas', 'Moreau', 'lucas.moreau@hrpulse.com', '+33 6 11 22 33 44',
            'M', 'MARIE', 'FIN', 'Responsable Financier', 'CDI', 4500, date(2020, 9, 1), None, None,
            'Audit, Trésorerie, Fiscalité, Modélisation financière', 'Boursorama Banque', 'FR76 4061 8802 6400 0011 2233 445',
            'Elodie Moreau', 'Épouse', '+33 6 12 99 88 77', 'AB+'
        ),
        (
            'EMP-2026-0005', 'Emma', 'Bernard', 'emma.bernard@hrpulse.com', '+33 6 77 88 99 00',
            'F', 'CELIBATAIRE', 'MKT', 'Growth Marketer & SEO', 'CDD', 3200, date(2026, 2, 15), date.today() + timedelta(days=20), None,
            'Google Ads, SEO, Copywriting, Google Analytics 4, Hubspot', 'LCL', 'FR76 3000 2000 1000 5566 7788 990',
            'Thomas Bernard', 'Frère', '+33 6 77 00 11 22', 'O-'
        ),
        (
            'EMP-2026-0006', 'Antoine', 'Rousseau', 'antoine.rousseau@hrpulse.com', '+33 6 33 22 11 00',
            'M', 'CELIBATAIRE', 'SALES', 'Business Developer B2B', 'CDI', 3400, date(2026, 7, 1), None, date.today() + timedelta(days=45),
            'Prospection B2B, Closing, CRM Salesforce, Négociation', 'CIC', 'FR76 3005 6000 0100 9988 7766 554',
            'Julie Rousseau', 'Mère', '+33 6 33 99 88 77', 'A-'
        ),
    ]

    employees = []
    for reg, fn, ln, email, phone, gender, marital, dept_code, pos_title, contract, salary, hire_d, end_d, prob_d, skills, bank, iban, ec_name, ec_rel, ec_phone, blood in employees_data:
        pos_obj = positions.get(pos_title)
        emp, created = Employee.objects.get_or_create(
            email=email,
            defaults={
                'registration_number': reg,
                'first_name': fn,
                'last_name': ln,
                'phone': phone,
                'gender': gender,
                'marital_status': marital,
                'department': depts[dept_code],
                'position': pos_obj,
                'contract_type': contract,
                'status': 'ACTIF',
                'hire_date': hire_d,
                'contract_end_date': end_d,
                'probation_end_date': prob_d,
                'base_salary': salary,
                'address': '15 Rue de la Paix',
                'city': 'Paris',
                'postal_code': '75002',
                'blood_group': blood,
                'skills': skills,
                'bank_name': bank,
                'iban': iban,
                'swift_bic': bank[:4].upper() + 'FRPP',
                'emergency_contact_name': ec_name,
                'emergency_contact_relation': ec_rel,
                'emergency_contact_phone': ec_phone,
            }
        )
        if not created:
            emp.registration_number = reg
            emp.blood_group = blood
            emp.skills = skills
            emp.bank_name = bank
            emp.iban = iban
            emp.swift_bic = bank[:4].upper() + 'FRPP'
            emp.emergency_contact_name = ec_name
            emp.emergency_contact_relation = ec_rel
            emp.emergency_contact_phone = ec_phone
            emp.city = 'Paris'
            emp.postal_code = '75002'
            if end_d:
                emp.contract_end_date = end_d
            if prob_d:
                emp.probation_end_date = prob_d
            emp.save()
        employees.append(emp)
        if created:
            print(f"👤 Employé créé: {emp.full_name} ({reg})")

    # Set Managers
    emp_dict = {e.registration_number: e for e in Employee.objects.all()}
    if 'EMP-2026-0001' in emp_dict:
        depts['RH'].manager = emp_dict['EMP-2026-0001']
        depts['RH'].save()
    if 'EMP-2026-0002' in emp_dict:
        depts['IT'].manager = emp_dict['EMP-2026-0002']
        depts['IT'].save()
        if 'EMP-2026-0003' in emp_dict:
            emp_dict['EMP-2026-0003'].manager = emp_dict['EMP-2026-0002']
            emp_dict['EMP-2026-0003'].save()
    if 'EMP-2026-0004' in emp_dict:
        depts['FIN'].manager = emp_dict['EMP-2026-0004']
        depts['FIN'].save()

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
    if len(employees) >= 5 and l_types:
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

    # 7. Payslips
    for emp in Employee.objects.all():
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

    # 8. Attendance Records
    today = date.today()
    for emp in Employee.objects.all():
        Attendance.objects.get_or_create(
            employee=emp,
            date=today,
            defaults={
                'time_in': '08:45:00',
                'time_out': '17:30:00',
                'status': 'PRESENT',
                'notes': 'Pointage automatique badge'
            }
        )
    print("🎉 Base de données initialisée avec succès !")

if __name__ == '__main__':
    seed()
