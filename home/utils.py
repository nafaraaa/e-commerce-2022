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
    #def ini fungsinya untuk memproses order yg sudah di kirimkan
    cart = cartData(request)
    if request.user.is_authenticated:
        try:
            order = Order.objects.filter(id=cart['order'].id).update(complete=True)
            print('sip')
        except :
            print('Asw')

base = 'https://api.whatsapp.com/send?phone=6281388762268&text='
def whatsappLinkCheckout(request,context):
    # context yg diambil adalah queryset dari list product yg dicheckout oleh pengguna
    productName = [item.product.title for item in context]
    productNumber = [item.quantity for item in context]
    #Dua variable ini digunakan untuk menampung list nama product yg akan dibeli 
    
    title = ""
    for i,a in zip(productName,productNumber):
        title += str(i) +" Jumlahnya: "+ str(a)
        title += ', '

    textWA = f'Permisi Bu aryani Saya ingin memesan:%0A{title}%0ADikirim Ke :%0ACatatan :%0ASekian Terimakasih.'
    linked = {'link':base + textWA.replace(' ', '%20')}
    return linked

def whatsappLinkBuyNow(request,context):
    product = context["object"]

    textWA = f'Permisi Bu aryani Saya ingin memesan:%0A{product.title}%0AJumlahnya :%0ADikirim Ke :%0ACatatan :%0ASekian Terimakasih.'
    linked = {'link':base + textWA.replace(' ', '%20')}
    print(linked['link'])
    return linked