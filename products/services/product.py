from ..models import Product
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict


def list(page_number):
    products = Product.objects.all().order_by('name')
    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page_number)
    products_list = [model_to_dict(product) for product in page_obj]
    return {
        'products': products_list,
        'page_info': {
            'number': page_obj.number,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
    }


def create(name, price, quantity):
    return Product.objects.create(name=name, price=price, quantity=quantity)


def retrieve(pk):
    product = get_object_or_404(Product, pk=pk)
    return model_to_dict(product)


def update(pk, data):
    product = get_object_or_404(Product, pk=pk)
    for field, value in data.items():
        setattr(product, field, value)
    product.save()
    return model_to_dict(product)


def delete(pk):
    # TODO: This should be soft deleted
    product = get_object_or_404(Product, pk=pk)
    product.delete()
