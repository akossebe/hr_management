from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('portal/', views.employee_portal_view, name='employee_portal'),
    path('portal/quick-punch/', views.quick_attendance_punch, name='quick_attendance_punch'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
