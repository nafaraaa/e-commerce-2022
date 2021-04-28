from .models import *


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        # items adalah class order yang
        # mengambil products dari orderitem yang
        # memiliki hubungan dengan order dari salah satu user
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

    items = context
    if len(context) > 1 or context == 0:
        # context yg diambil adalah queryset dari list product yg dicheckout oleh pengguna
        productName = [item.product.title for item in items]
        productNumber = [item.quantity for item in items]
        #Dua variable ini digunakan untuk menampung list nama product yg akan dibeli 
        
        title = ""
        for i,a in zip(productName,productNumber):
            title += str(i) +" Jumlahnya: "+ str(a)
            title += ', '

        textWA = f'Permisi Bu aryani Saya ingin memesan:%0A{title}%0ADikirim Ke :%0ACatatan :%0ASekian Terimakasih.'
        linked = {'link':base + textWA.replace(' ', '%20')}
        return linked
    else:
        return {'link':'Failed'}

def checkUser(request):
    userr = False
    if str(request.user) == 'AnonymousUser':
        userr = True
        print(request.user)
        return {'hai':'hai','is_user':'tidak ada'}
    return {'hai':'hai'}

def paginationFilter(request):
    full_path = request.get_full_path()
    yolo = False
    if len(request.GET) != 0:
        yolo = True
        return {'path':full_path,'aye':yolo}
    return {'aye':yolo}
    
def whatsappLinkBuyNow(request,context):
    product = context["product"]
    textWA = f'Permisi Bu aryani Saya ingin memesan:%0A{product.title}%0AJumlahnya :%0ADikirim Ke :%0ACatatan :%0ASekian Terimakasih.'
    linked = {'link':base + textWA.replace(' ', '%20')}
    return linked

def mergeFunction(request,context):
    dictionary = {}
    dictionary.update(whatsappLinkCheckout(request,context))
    dictionary.update(paginationFilter(request))
    dictionary.update(checkUser(request))
    return dictionary