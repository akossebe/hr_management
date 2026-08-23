from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
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


class EmployeeViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        self.dept = Department.objects.create(name="Ressources Humaines", code="RH")
        self.pos = Position.objects.create(
            title="Gestionnaire RH",
            department=self.dept,
            base_salary_min=2500,
            base_salary_max=4000
        )
        self.employee = Employee.objects.create(
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
