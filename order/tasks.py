from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task

from order.models import Order, User, OrderItem


@shared_task
def send_email(order_id, message):
    order = Order.objects.get(id=order_id)
    subject = f"Bizning do'konimizdan mahsulot sotib olayabsiz"
    send_message = (f"Hurmatli {order.customer.username}\n"
                    f"Siz quyidagi mahsulotlarni sotib olmoqdasiz: \n\n") + message
    mailer = send_mail(subject, send_message, settings.EMAIL_HOST_USER, [order.customer.email, ])
    orderitems = OrderItem.objects.filter(customer=order.customer)
    order.orderitem.clear()
    orderitems.delete()
    order.delete()
    return mailer
