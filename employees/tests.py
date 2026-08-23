from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import date, timedelta
from employees.models import Department, Position, Employee, EmployeeDocument


class EmployeeModelTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="IT & Tech", code="IT")
        self.pos = Position.objects.create(
            title="Software Engineer",
            department=self.dept,
            base_salary_min=3000,
            base_salary_max=5000
        )
        self.employee = Employee.objects.create(
            first_name="Jean",
            last_name="Valjean",
            email="jean.valjean@entreprise.com",
            phone="+33612345678",
            department=self.dept,
            position=self.pos,
            contract_type="CDI",
            status="ACTIF",
            hire_date=date(2022, 1, 1),
            date_of_birth=date(1990, 5, 20),
            base_salary=4000
        )

    def test_employee_creation_and_matricule(self):
        self.assertTrue(self.employee.registration_number.startswith("EMP-"))
        self.assertEqual(self.employee.full_name, "Jean Valjean")
        self.assertGreater(self.employee.age, 30)
        self.assertGreater(self.employee.seniority_years, 2)

    def test_department_payroll_and_count(self):
        self.assertEqual(self.dept.employee_count(), 1)
        self.assertEqual(self.dept.total_payroll, 4000)


class EmployeeAuthAndViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword', email='admin@hr.com')
        self.client.login(username='admin', password='adminpassword')

        self.dept = Department.objects.create(name="Ressources Humaines", code="RH")
        self.pos = Position.objects.create(
            title="Gestionnaire RH",
            department=self.dept,
            base_salary_min=2500,
            base_salary_max=4000
        )
        
        # User associé à l'employé
        self.emp_user = User.objects.create_user(
            username='sophie.durand',
            email='sophie.durand@entreprise.com',
            password='secretpassword123'
        )
        self.employee = Employee.objects.create(
            user=self.emp_user,
            first_name="Sophie",
            last_name="Durand",
            email="sophie.durand@entreprise.com",
            phone="+33699887766",
            department=self.dept,
            position=self.pos,
            contract_type="CDI",
            status="ACTIF",
            hire_date=date.today() - timedelta(days=200),
            base_salary=3200
        )

    def test_multi_identifier_auth_backend(self):
        # 1. Connexion par username
        user1 = authenticate(username='sophie.durand', password='secretpassword123')
        self.assertIsNotNone(user1)

        # 2. Connexion par email
        user2 = authenticate(username='sophie.durand@entreprise.com', password='secretpassword123')
        self.assertIsNotNone(user2)
        self.assertEqual(user1, user2)

        # 3. Connexion par matricule
        user3 = authenticate(username=self.employee.registration_number, password='secretpassword123')
        self.assertIsNotNone(user3)
        self.assertEqual(user1, user3)

    def test_employee_portal_view(self):
        # Connexion en tant que Sophie Durand (employé simple)
        self.client.logout()
        self.client.login(username='sophie.durand', password='secretpassword123')
        response = self.client.get(reverse('employee_portal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sophie")
        self.assertContains(response, "Espace Collaborateur")

    def test_employee_manage_account_view(self):
        response = self.client.post(
            reverse('employee_manage_account', kwargs={'pk': self.employee.pk}),
            {
                'username': 'sophie.durand.updated',
                'password': 'newsecretpassword456',
                'is_active': True,
                'is_staff': True
            }
        )
        self.assertEqual(response.status_code, 302)
        self.emp_user.refresh_from_db()
        self.assertEqual(self.emp_user.username, 'sophie.durand.updated')
        self.assertTrue(self.emp_user.check_password('newsecretpassword456'))
        self.assertTrue(self.emp_user.is_staff)

    def test_employee_list_view(self):
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sophie Durand")

    def test_employee_detail_view(self):
        response = self.client.get(reverse('employee_detail', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sophie Durand")
        self.assertContains(response, "Gestionnaire RH")

    def test_employee_badge_view(self):
        response = self.client.get(reverse('employee_badge', kwargs={'pk': self.employee.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Carte Professionnelle")

    def test_employee_org_chart_view(self):
        response = self.client.get(reverse('employee_org_chart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Organigramme")

    def test_export_csv_view(self):
        response = self.client.get(reverse('employee_export_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8-sig')
        self.assertIn('Sophie', response.content.decode('utf-8-sig'))

    def test_position_list_view(self):
        response = self.client.get(reverse('position_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gestionnaire RH")

    def test_department_detail_view(self):
        response = self.client.get(reverse('department_detail', kwargs={'pk': self.dept.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ressources Humaines")
