from django.urls import path
from . import views

urlpatterns = [
    path('', views.PayslipListView.as_view(), name='payslip_list'),
    path('add/', views.PayslipCreateView.as_view(), name='payslip_add'),
    path('<int:pk>/', views.PayslipDetailView.as_view(), name='payslip_detail'),
    path('<int:pk>/edit/', views.PayslipUpdateView.as_view(), name='payslip_edit'),
    path('<int:pk>/delete/', views.PayslipDeleteView.as_view(), name='payslip_delete'),
]
