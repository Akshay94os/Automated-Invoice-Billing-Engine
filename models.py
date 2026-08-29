from django.db import models

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    client_name = models.CharField(max_length=150)
    client_email = models.EmailField()
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return sum(item.total_price() for item in self.items.all())

    def total_due(self):
        sub = self.subtotal()
        tax = sub * (self.tax_percent / 100)
        return round(sub + tax, 2)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client_name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def total_price(self):
        return self.quantity * self.unit_price
