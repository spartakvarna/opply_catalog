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
    """List orders for customer chronologically.

    curl -X GET http://127.0.0.1:8000/catalog/orders/list/1/
    """
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)

    orders = Order.objects.filter(customer=customer).order_by('-datetime')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    orders_list = [model_to_dict(order) for order in page_obj]
    return JsonResponse({'orders': orders_list}, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    """Create an order.

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

        if 'customer_id' not in data or 'product_id' not in data:
            missing_fields = [field for field in ['customer_id', 'product_id'] if field not in data]
            return JsonResponse({'error': f'Missing fields: {", ".join(missing_fields)}'}, status=400)

        customer = Customer.objects.get(pk=data['customer_id'])
        product = Product.objects.get(pk=data['product_id'])

        if product.quantity < data['quantity']:
            return JsonResponse({'error': 'Not enough product in stock'}, status=400)
        data_price_decimal = Decimal(str(data['price']))

        if product.price != data_price_decimal:
            return JsonResponse({'error': 'Price has changed, please order again with the current price'}, status=400)

        order = Order.objects.create(
            customer=customer,
            product=product,
            price=data_price_decimal,
            quantity=data['quantity'],
            datetime=timezone.now()
        )

        product.quantity -= data['quantity']
        product.save()

        return JsonResponse(model_to_dict(order), status=201)

    except KeyError as e:
        return JsonResponse({'error': f'Missing field: {str(e)}'}, status=400)
    except (Product.DoesNotExist, Customer.DoesNotExist) as e:
        return JsonResponse({'error': str(e)}, status=404)
    except ValueError as e:
        return JsonResponse({'error': 'Invalid data provided'}, status=400)
