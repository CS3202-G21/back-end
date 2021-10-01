from django.urls import path, include
from .api import CustomerOrderViewSet, CustomerOrderUpdateViewSet, CustomerOrderPaymentSuccessViewSet, GetCustomerOrdersViewSet, AddOrderReviewViewSet, GetOrderReviewsViewSet


urlpatterns = [
    path('api/order', CustomerOrderViewSet.as_view()),
    path('api/order/update', CustomerOrderUpdateViewSet.as_view()),
    path('api/order/payment_success', CustomerOrderPaymentSuccessViewSet.as_view()),
    path('api/order/get_orders', GetCustomerOrdersViewSet.as_view()),
    path('api/order/add_review', AddOrderReviewViewSet.as_view()),
    path('api/order/get_reviews', GetOrderReviewsViewSet.as_view()),
]