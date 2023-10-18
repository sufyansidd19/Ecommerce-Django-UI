import json
from django.shortcuts import render
from .models import Product, Contact, Orders , OrderUpdate
from math import ceil
from django.db.models import Count
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.
from django.http import HttpResponse

# def index(request):
#     products= Product.objects.all()
#     allProds=[]
#     catprods= Product.objects.values('category', 'id')
#     cats= {item["category"] for item in catprods}
#     for cat in cats:
#         prod=Product.objects.filter(category=cat)
#         n = len(prod)
#         nSlides = n // 4 + ceil((n / 4) - (n // 4))
#         allProds.append([prod, range(1, nSlides), nSlides])

#     params={'allProds':allProds }
#     return render(request,"shop/index.html", params)

def index(request):
    # Group products by category and count the number of products per category
    categories_with_products = Product.objects.values('category').annotate(product_count=Count('id'))

    # Fetch limited number of products per category (assuming 6 products per category)
    products_by_category = {}
    for category_info in categories_with_products:
        category = category_info['category']
        products = Product.objects.filter(category=category)[:6]  # Change the limit as needed
        products_by_category[category] = products

    return render(request, 'shop/index.html', {'products_by_category': products_by_category})

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank=False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    return render(request, 'shop/contact.html' , {'thank':thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates , order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'Shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')

def productView(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)


    return render(request, 'shop/prodView.html', {'product':product[0]})

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        update= OrderUpdate(order_id= order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'shop/checkout.html')
