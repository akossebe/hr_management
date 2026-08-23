from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet, DepartmentViewSet, PositionViewSet,
    LeaveRequestViewSet, PayslipViewSet, AttendanceViewSet
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'leaves', LeaveRequestViewSet)
router.register(r'payslips', PayslipViewSet)
router.register(r'attendances', AttendanceViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
