from .models import *


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        print(order.get_cart_totals)
    else:
        items = []
    return {'items':items, 'order':order}
