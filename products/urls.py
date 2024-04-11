from django.urls import path
from .views.products_views import product_list, product_create, get_product, update_product, delete_product
from .views.orders_view import list_orders, create_order
from .views.auth_view import ObtainTokenView, RevokeTokenView


urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/create/', product_create, name='product_create'),
    path('products/<int:pk>/', get_product, name='get_product'),
    path('products/<int:pk>/update/', update_product, name='update_product'),
    path('products/<int:pk>/delete/', delete_product, name='delete_product'),
    path('orders/list/<int:customer_id>/', list_orders, name='list_orders'),
    path('orders/create/', create_order, name='create_order'),
    path('api/token/', ObtainTokenView.as_view(), name='obtain_token'),
    path('api/token/revoke/', RevokeTokenView.as_view(), name='revoke_token'),
]
