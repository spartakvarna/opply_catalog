from ..models import Product
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict


def get_all(page_number):
    """Get all products of a specific page or the first page if page_number is None.

    Each page has 10 rows.
    """
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
    try:
        product = Product.objects.get(pk=pk)
        return model_to_dict(product)
    except Product.DoesNotExist:
        return None


def get_by_name(name):
    try:
        product = Product.objects.get(name=name)
        return product
    except Product.DoesNotExist:
        return None


def update(pk, name=None, price=None, quantity=None):
    try:
        product = Product.objects.get(pk=pk)

        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        if quantity is not None:
            product.quantity = quantity

        product.save()
        return model_to_dict(product)
    except Product.DoesNotExist:
        return None


def delete(pk):
    try:
        product = Product.objects.get(pk=pk)
        product.delete()
        return True
    except Product.DoesNotExist:
        return None
