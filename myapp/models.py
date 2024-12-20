from django.db import models

class Invoice(models.Model):
    fr_date = models.DateField(verbose_name="FR Date")
    company_code = models.CharField(max_length=50, verbose_name="Company Code")
    plant_code = models.CharField(max_length=50, verbose_name="Plant Code", null=True, blank=True)
    vendor_name = models.CharField(max_length=255, verbose_name="Vendor Name")
    vendor_code = models.CharField(max_length=50, verbose_name="Vendor Code")
    quantity = models.IntegerField(verbose_name="Quantity")
    po_number = models.CharField(max_length=50, verbose_name="PO Number")
    material_document_number = models.CharField(max_length=50, verbose_name="Material Document Number")
    gl_account_number = models.CharField(max_length=50, verbose_name="GL Account Number")
    currency = models.CharField(max_length=10, verbose_name="Currency")
    invoice = models.CharField(max_length=50, verbose_name="Invoice")
    invoice_dt = models.DateField(verbose_name="Invoice Date")
    invoice_amt = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Invoice Amount")
    tds = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="TDS")
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fr_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="FR Amount")
    approval1 = models.CharField(max_length=50, default="waiting", verbose_name="Approval 1")
    approval2 = models.CharField(max_length=50, default="waiting", verbose_name="Approval 2")
    commentsAPP1 = models.TextField(null=True, blank=True, verbose_name="CommentsAPP1")
    commentsAPP2 = models.TextField(null=True, blank=True, verbose_name="CommentsAPP2")

    def __str__(self):
        return f"Invoice {self.invoice} - {self.vendor_name}"

