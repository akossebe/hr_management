from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, Department, Position, EmployeeDocument


class EmployeeDocumentInline(admin.TabularInline):
    model = EmployeeDocument
    extra = 1
    fields = ['title', 'document_type', 'file', 'expiry_date', 'notes']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'avatar_preview', 'registration_number', 'full_name',
        'department', 'position', 'contract_type', 'status', 'hire_date'
    ]
    list_filter = ['status', 'contract_type', 'department', 'gender', 'marital_status']
    search_fields = ['first_name', 'last_name', 'registration_number', 'email', 'phone', 'skills']
    inlines = [EmployeeDocumentInline]
    
    fieldsets = (
        ('Identité & État Civil', {
            'fields': (
                ('first_name', 'last_name'),
                ('registration_number', 'photo'),
                ('date_of_birth', 'place_of_birth', 'nationality'),
                ('gender', 'marital_status', 'blood_group'),
                'national_id_number',
            )
        }),
        ('Coordonnées & Adresse', {
            'fields': (
                ('email', 'personal_email'),
                'phone',
                'address',
                ('city', 'postal_code'),
            )
        }),
        ('Contact d\'Urgence', {
            'fields': (
                ('emergency_contact_name', 'emergency_contact_relation'),
                'emergency_contact_phone',
            )
        }),
        ('Affectation Professionnelle', {
            'fields': (
                ('department', 'position'),
                'manager',
                ('contract_type', 'status'),
                ('hire_date', 'probation_end_date', 'contract_end_date'),
            )
        }),
        ('Rémunération & Coordonnées Bancaires', {
            'fields': (
                'base_salary',
                ('bank_name', 'iban', 'swift_bic'),
            )
        }),
        ('Compétences & Notes RH', {
            'fields': (
                'skills',
                'notes',
            )
        }),
    )

    def avatar_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return format_html('<span style="display:inline-block; width:36px; height:36px; line-height:36px; text-align:center; border-radius:50%; background:#e0e7ff; color:#3730a3; font-weight:bold;">{}{}</span>', obj.first_name[:1], obj.last_name[:1])
    avatar_preview.short_description = 'Photo'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'manager', 'employee_count', 'created_at']
    search_fields = ['name', 'code', 'description']


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'base_salary_min', 'base_salary_max', 'employee_count']
    list_filter = ['department']
    search_fields = ['title', 'description']


@admin.register(EmployeeDocument)
class EmployeeDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'employee', 'document_type', 'expiry_date', 'uploaded_at']
    list_filter = ['document_type', 'expiry_date']
    search_fields = ['title', 'employee__first_name', 'employee__last_name', 'employee__registration_number']
