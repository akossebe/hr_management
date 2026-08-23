from django.urls import path
from . import views

urlpatterns = [
    path('', views.AttendanceListView.as_view(), name='attendance_list'),
    path('add/', views.AttendanceCreateView.as_view(), name='attendance_add'),
]
