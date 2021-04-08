from .models import *


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        # items adalah class order yang
        # mengambil products dari orderitem yang
        # memiliki hubungan dengan order dari salah satu user
        print(order.id,'anjayy')
    else:
        items = []
        order = {'get_cart_items':'0','get_cart_totals':'0'}
        items = order['get_cart_totals']
    return {'items':items, 'order':order}

def CompleteOrder(request):
    cart = cartData(request)
    if request.user.is_authenticated:
        try:
            order = Order.objects.filter(id=cart['order'].id).update(complete=True)
            print('sip')
        except :
            print('Asw')
        
