from django.shortcuts import render,get_object_or_404
from .models import Item,OrderItem,Order
from django.views.generic import ListView,DetailView


def products(request):
    context =   {
        'items' :   Item.objects.all()
    }
    return render(request,'product.html',context)

def checkout(request):
    return render(request,'checkout.html')

class HomeView(ListView):
    model = Item
    template_name = "home.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

def add_to_cart(request,slug):
    item    =   get_object_or_404(Item, slug=slug)
    order_item  =   OrderItem.objects.create(item=item)
    order_qs   =   Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order   =   order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order.item.save()
    else:
        order_item  =   Order.objects.create(user=request.user)
        order.items.add(order_item)

