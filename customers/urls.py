from django.urls import path, include
from .api import RegisterCustomerAPI, LoginCustomerAPI, CustomerAPI
from knox import views as knox_views

urlpatterns = [
    path('api/auth/customer', include('knox.urls')),
    path('api/auth/customer/register', RegisterCustomerAPI.as_view()),
    path('api/auth/customer/login', LoginCustomerAPI.as_view(), name='customer-login'),
    path('api/auth/customer/user', CustomerAPI.as_view()),
    path('api/auth/customer/logout', knox_views.LogoutView.as_view(), name='knox_logout')
]