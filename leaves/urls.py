from django.urls import path
from . import views

urlpatterns = [
    path('', views.LeaveListView.as_view(), name='leave_list'),
    path('add/', views.LeaveCreateView.as_view(), name='leave_add'),
    path('<int:pk>/status/', views.LeaveUpdateStatusView.as_view(), name='leave_status'),
]
