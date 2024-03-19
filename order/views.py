from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

from .models import (
    Order,
    OrderItem
)

from product.models import Product
from .tasks import send_email


@login_required(login_url='/accounts/login/')
def order_summary(request):
    order = Order.objects.filter(customer=request.user, ordered=False).annotate(
        order_total_price=Sum('orderitem__total_price'),
    ).first()
    if order is not None:
        if order.order_total_price is None:
            order.order_total_price = 0
            context = {'order': 0.00, 'discount': 0.00, 'total': 0.00}
        else:
            discount = round(float(order.order_total_price) * 0.01, 3)
            total = float(order.order_total_price) - discount
            context = {
                'order': order,
                'discount': discount,
                'total': total,
            }
    else:
        context = {'order': 0.00, 'discount': 0.00, 'total': 0.00}
    return render(request, 'order/cart.html', context)


@login_required()
def checkout(request):
    order = Order.objects.filter(customer=request.user, ordered=False).annotate(
        order_total_price=Sum('orderitem__total_price'),
    ).first()

    if order is None:
        return render(request, 'order/checkout.html', context={"message": "Sizda sotib olingan buyumlar yo'q"})
    discount = round(float(order.order_total_price) * 0.01, 3)
    total = float(order.order_total_price) - discount
    message = ""
    orderitems = OrderItem.objects.filter(customer=request.user, ordered=False)
    for orderitem in orderitems:
        message += (f"Mahsulot nomi: {orderitem.product.title}\n"
                    f"Mahsulot soni: {orderitem.quantity}\n"
                    f"Mahsulot rangi: {orderitem.product.color}\n"
                    f"Mahsulot o'lchami: {orderitem.product.size}\n"
                    f"Bitta Mahsulotning narxi: ${orderitem.product.price}\n\n\n")
    message += f"Mahsulotlarning umumiy narxi: ${order.order_total_price}\n\n"
    message += f"Siz uchun chegirma: ${float(discount)}\n\n"
    message += f"To'lashingiz kerak bo'lgan narx: ${total}\n\n"
    send_email.delay(order.id, message)
    return render(request, 'order/checkout.html')


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        customer=request.user,
    )

    order_qs = Order.objects.filter(customer=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.orderitem.filter(product__pk=product.pk).exists():
            messages.info(request, "Mahsulot oldin savatingizga qo'shilgan")
            return redirect("product:product_list")
        else:
            order.orderitem.add(order_item)
            messages.info(request, "Mahsulot savatingizga qo'shildi")
            return redirect("product:product_list")
    else:
        order = Order.objects.create(customer=request.user)
        # send_email.delay(order.id, product)
        order.orderitem.add(order_item)
        messages.info(request, "Mahsulot savatingizga qo'shildi")
        return redirect("order:order_summary")


# def buy(request)


@login_required
def remove_from_cart(request, pk):
    order_item = OrderItem.objects.get(pk=pk)
    order = order_item.order_set.all().first()
    if order:
        order.orderitem.remove(order_item)
        order_item.delete()
    return redirect("order:order_summary")


@login_required
def reduce_quantity_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitem.filter(product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                customer=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.product.quantity += 1
                order_item.product.save()
                order_item.save()
                messages.info(request, "Mahsulotingiz soni 1 taga kamaytirildi")
            else:
                order_item.delete()
                messages.info(request, "Mahsulot savatingizdan o'chirldi")
            return redirect("order:order_summary")
        else:
            messages.info(request, "Sizning savatingizda ushbu mahsulot mavjud emas")
            return redirect("order:order_summary")
    else:
        # add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("order:order_summary")


@login_required
def increase_quantity_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        customer=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.orderitem.filter(product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                customer=request.user,
                ordered=False
            )[0]
            if order_item.quantity < 10 and order_item.product.quantity >= 1:
                order_item.quantity += 1
                order_item.product.quantity -= 1
                order_item.product.save()
                order_item.save()
            elif order_item.product.quantity == 0:
                messages.info(request, "Bu Tovardan boshqa qolmagan")
                return redirect("order:order_summary")
            else:
                messages.info(request, "10 tadan ko'p olish mumkin emas")
                return redirect("order:order_summary")
            messages.info(request, "Mahsulot soni 1 taga ko'paytirildi")
            return redirect("order:order_summary")
        else:
            messages.info(request, "Bu mahsulot sizni savatingizda mavjud emas")
            return redirect("order:order_summary")
    else:
        messages.info(request, "Savatingiz bo'sh")
        return redirect("order:order_summary")
