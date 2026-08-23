from django.urls import path
from . import views

urlpatterns = [
    # Employee Management
    path('', views.EmployeeListView.as_view(), name='employee_list'),
    path('add/', views.EmployeeCreateView.as_view(), name='employee_add'),
    path('export/csv/', views.export_employees_csv, name='employee_export_csv'),
    path('orgchart/', views.OrgChartView.as_view(), name='employee_org_chart'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee_edit'),
    path('<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('<int:pk>/badge/', views.EmployeeBadgeView.as_view(), name='employee_badge'),
    path('<int:pk>/account/manage/', views.EmployeeManageAccountView.as_view(), name='employee_manage_account'),
    
    # Documents
    path('<int:pk>/documents/upload/', views.EmployeeDocumentUploadView.as_view(), name='employee_document_upload'),
    path('<int:pk>/documents/<int:doc_pk>/delete/', views.EmployeeDocumentDeleteView.as_view(), name='employee_document_delete'),
    
    # Departments
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/add/', views.DepartmentCreateView.as_view(), name='department_add'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('departments/<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_edit'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),
    
    # Positions (Postes)
    path('positions/', views.PositionListView.as_view(), name='position_list'),
    path('positions/add/', views.PositionCreateView.as_view(), name='position_add'),
    path('positions/<int:pk>/edit/', views.PositionUpdateView.as_view(), name='position_edit'),
    path('positions/<int:pk>/delete/', views.PositionDeleteView.as_view(), name='position_delete'),
]
