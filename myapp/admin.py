from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'fr_date', 'company_code', 'vendor_name', 'invoice', 'invoice_dt', 
        'invoice_amt', 'approval1', 'approval2'
    )
    list_filter = ('fr_date', 'approval1', 'approval2', 'currency', 'company_code')
    search_fields = ('vendor_name', 'invoice', 'po_number', 'material_document_number', 'company_code')
