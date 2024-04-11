from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
import json
from django.views.decorators.csrf import csrf_exempt
from ..services import product as product_service



@csrf_exempt
@require_http_methods(["GET"])
def product_list(request):
    """List all products.

    - Request parameters: None
    - Query parameters: page (int, optional) - Page number for pagination.
    - Possible response HTTP codes: 200 (OK)

    curl -X GET http://127.0.0.1:8000/catalog/products/
    """

    page_number = request.GET.get('page')
    result = product_service.list(page_number)
    return JsonResponse(result)

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

    try:
        data = json.loads(request.body)
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')

        if name is None or price is None or quantity is None:
            return JsonResponse({'error': 'Missing required parameters'}, status=400)

        product = product_service.create(name, price, quantity)

        return JsonResponse(model_to_dict(product), status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def get_product(request, pk):
    """Retrieve a product.

    - URL parameters: pk (int) - The primary key of the product to retrieve.
    - Possible response HTTP codes: 200 (OK), 404 (Not Found)

    curl -X GET http://127.0.0.1:8000/catalog/products/1/
    """

    product_data = product_service.retrieve(pk)
    return JsonResponse(product_data)


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

    data = json.loads(request.body)
    updated_product_data = product_service.update(pk, data)
    return JsonResponse(updated_product_data)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product(request, pk):
    """Delete a product.

    - URL parameters: pk (int) - The primary key of the product to delete.
    - Possible response HTTP codes: 204 (No Content), 404 (Not Found)

    curl -X DELETE http://127.0.0.1:8000/catalog/products/1/delete/
    """
    product_service.delete(pk)
    return HttpResponse(status=204)
