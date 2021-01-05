from django.shortcuts import render
from phones.models import Phone


def show_catalog(request, sort='name'):
    if sort == 'name':
        products = Phone.objects.order_by('name')
    elif sort == 'min_price':
        products = Phone.objects.order_by('price')
    elif sort == 'max_price':
        products = Phone.objects.order_by('-price')
    return render(
        request, 'catalog.html', {'products': products, 'sort': sort}
        )


def show_product(request, slug):
    product = Phone.objects.get(slug=slug)
    return render(request, 'product.html', {'product': product})
