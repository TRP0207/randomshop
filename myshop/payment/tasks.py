from io import BytesIO
from celery import task
import weasyprint
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order


@task
def payment_completed(order_id):
    """
    task to send an email notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)

    #create invoice email
    subject = f'My Shop - EE Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])

    #generate PDF
    html = render_to_string('admin/orders/order/pdf.html', {'order': order})
    out =BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    #attach PDf file
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

    #send email
    email.send()
















