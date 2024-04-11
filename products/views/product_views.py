from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from ..models import Product
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_http_methods(["GET"])
def product_list(request):
    """List all products.

    - Request parameters: None
    - Query parameters: page (int, optional) - Page number for pagination.
    - Possible response HTTP codes: 200 (OK)

    curl -X GET http://127.0.0.1:8000/catalog/products/
    """

    products = Product.objects.all().order_by('name')
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    products_list = [model_to_dict(product) for product in page_obj]
    return JsonResponse({'products': products_list, 'page_info': {
        'number': page_obj.number,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    }})

@csrf_exempt
@require_http_methods(["POST"])
def product_create(request):
    """Create a new product.

    - Request parameters (JSON body):
      - name (str): Name of the product.
      - price (float): Price of the product.
      - quantity (int): Available quantity of the product.
    - Possible response HTTP codes: 201 (Created)

    curl -X POST http://127.0.0.1:8000/catalog/products/create/ \
    -H "Content-Type: application/json" \
    -d '{"name": "New Product", "price": 19.99, "quantity": 100}'
    """

    data = json.loads(request.body)
    product = Product.objects.create(**data)
    return JsonResponse(model_to_dict(product), status=201)

@csrf_exempt
@require_http_methods(["GET"])
def get_product(request, pk):
    """Retrieve a product.

    - URL parameters: pk (int) - The primary key of the product to retrieve.
    - Possible response HTTP codes: 200 (OK), 404 (Not Found)

    curl -X GET http://127.0.0.1:8000/catalog/products/1/
    """

    product = get_object_or_404(Product, pk=pk)
    return JsonResponse(model_to_dict(product))

@csrf_exempt
@require_http_methods(["PUT"])
def update_product(request, pk):
    """Update a product.

    - URL parameters: pk (int) - The primary key of the product to update.
    - Request parameters (JSON body):
      - name (str, optional): New name of the product.
      - price (float, optional): New price of the product.
      - quantity (int, optional): New available quantity of the product.
    - Possible response HTTP codes: 200 (OK), 404 (Not Found)

    curl -X PUT http://127.0.0.1:8000/catalog/products/1/update/ \
    -H "Content-Type: application/json" \
    -d '{"name": "Updated Product Name", "price": 25.99, "quantity": 95}'
    """

    product = get_object_or_404(Product, pk=pk)
    data = json.loads(request.body)
    for field, value in data.items():
        setattr(product, field, value)
    product.save()
    return JsonResponse(model_to_dict(product))

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product(request, pk):
    """Delete a product.

    - URL parameters: pk (int) - The primary key of the product to delete.
    - Possible response HTTP codes: 204 (No Content), 404 (Not Found)

    curl -X DELETE http://127.0.0.1:8000/catalog/products/1/delete/
    """
    product = get_object_or_404(Product, pk=pk)
    # TODO: This should be soft deleted
    product.delete()
    return HttpResponse(status=204)

