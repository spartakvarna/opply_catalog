from django.utils import timezone
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

from ..models import Product


def get_all(page_number):
    """Get all active and not soft-deleted products of a specific page or the first page if page_number is None.

    Each page has 10 rows.
    """
    products = Product.objects.filter(deleted_at__isnull=True, is_active=True).order_by('name')
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
    """Create Product."""
    return Product.objects.create(name=name, price=price, quantity=quantity)


def retrieve(pk):
    """Get Product by id or None if such does not exist."""
    try:
        product = Product.objects.get(pk=pk)
        return model_to_dict(product)
    except Product.DoesNotExist:
        return None


def get_by_name(name):
    """Get Product by name or None if such does not exist."""
    try:
        product = Product.objects.get(name=name)
        return product
    except Product.DoesNotExist:
        return None


def update(pk, name=None, price=None, quantity=None):
    """Update Product fields.

    Updates for the values name, price, quantity which are not None.
    """
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
    """Delete Product from table.

    Cascadingly removes order (currently wrong).
    TODO: Implement soft delete"""
    try:
        # TODO: Implement soft delete
        product = Product.objects.get(pk=pk)
        product.delete()
        return True
    except Product.DoesNotExist:
        return None


def soft_delete(pk):
    """Soft delete a product by setting its deleted_at timestamp.

    Returns:
        True if successful, False if Product does not exist.
    """
    try:
        product = Product.objects.get(pk=pk)
        product.deleted_at = timezone.now()
        product.save()
        return True
    except Product.DoesNotExist:
        return False


def enable(pk):
    """Enable a product.

    Returns:
        True if successful, False if Product does not exist.
    """
    try:
        product = Product.objects.get(pk=pk)
        product.is_active = True
        product.save()
        return True
    except Product.DoesNotExist:
        return False


def disable(pk):
    """Disable a product.

    Returns:
        True if successful, False if Product does not exist.
    """
    try:
        product = Product.objects.get(pk=pk)
        product.is_active = False
        product.save()
        return True
    except Product.DoesNotExist:
        return False


def toggle_enabled(pk):
    """Toggle the enabled state of a product.

    Returns:
        True if successful, False if Product does not exist.
    """
    try:
        product = Product.objects.get(pk=pk)
        product.is_active = not product.is_active
        product.save()
        return True
    except Product.DoesNotExist:
        return False
