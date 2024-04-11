import json

from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from ..models import Product, Order, Customer


@csrf_exempt
@require_http_methods(["GET"])
def list_orders(request, customer_id):
    """
    List orders for a customer chronologically, excluding orders for soft-deleted products.

    curl -X GET http://127.0.0.1:8000/catalog/orders/list/1/
    """
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)

    # Filter orders by customer, excluding those linked to soft-deleted products
    orders = Order.objects.filter(customer=customer, product__deleted_at__isnull=True).order_by('-datetime')
    paginator = Paginator(orders, 10)  # Assuming you want to keep pagination
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    orders_list = [model_to_dict(order) for order in page_obj]
    return JsonResponse({'orders': orders_list}, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    """
    Create an order.

    curl -X POST http://127.0.0.1:8000/catalog/orders/create/ \
    -H "Content-Type: application/json" \
    -d '{
          "customer_id": 1,
          "product_id": 2,
          "price": 19.99,
          "quantity": 3
        }'
    """
    try:
        data = json.loads(request.body)

        # Check for missing required fields
        if 'customer_id' not in data or 'product_id' not in data or 'quantity' not in data or 'price' not in data:
            missing_fields = [field for field in ['customer_id', 'product_id', 'quantity', 'price'] if field not in data]
            return JsonResponse({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=400)

        # Fetch the customer and product while ensuring the product is not disabled or soft deleted
        customer = Customer.objects.get(pk=data['customer_id'])
        product = Product.objects.filter(pk=data['product_id'], is_active=True, deleted_at__isnull=True).first()

        if not product:
            return JsonResponse({'error': 'Product not available'}, status=404)

        # Validate product stock and price
        if product.quantity < data['quantity']:
            return JsonResponse({'error': 'Not enough product in stock'}, status=400)

        data_price_decimal = Decimal(str(data['price']))
        if product.price != data_price_decimal:
            return JsonResponse({'error': 'Price has changed, please order again with the current price'}, status=400)

        # Create the order
        order = Order.objects.create(
            customer=customer,
            product=product,
            price=data_price_decimal,
            quantity=data['quantity'],
            datetime=timezone.now()
        )

        # Update product stock
        product.quantity -= data['quantity']
        product.save()

        return JsonResponse(model_to_dict(order), status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except ValueError as e:
        return JsonResponse({'error': 'Invalid data provided'}, status=400)