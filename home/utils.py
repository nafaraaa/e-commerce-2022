from .models import *


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        # items adalah class order yang
        # mengambil products dari orderitem yang
        # memiliki hubungan dengan order dari salah satu user
        print(order.get_cart_totals)
    else:
        items = []
    return {'items':items, 'order':order}
