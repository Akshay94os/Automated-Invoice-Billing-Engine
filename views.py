from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice, InvoiceItem
import uuid

def index(request):
    if request.method == 'POST':
        client = request.POST.get('client_name')
        email = request.POST.get('client_email')
        tax = request.POST.get('tax_percent', 5.0)
        inv = Invoice.objects.create(
            invoice_number=f"INV-{uuid.uuid4().hex[:6].upper()}",
            client_name=client,
            client_email=email,
            tax_percent=tax
        )
        return redirect('invoice_detail', pk=inv.id)

    invoices = Invoice.objects.order_by('-created_at')
    return render(request, 'billing/index.html', {'invoices': invoices})

def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    if request.method == 'POST':
        desc = request.POST.get('description')
        qty = int(request.POST.get('quantity', 1))
        price = float(request.POST.get('unit_price', 0))
        InvoiceItem.objects.create(invoice=invoice, description=desc, quantity=qty, unit_price=price)
        return redirect('invoice_detail', pk=invoice.id)

    return render(request, 'billing/detail.html', {'invoice': invoice})
