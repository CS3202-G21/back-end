from django.urls import path, include
from .api import LoginStaffAPI, StaffAPI, RegisterStaffAPI
from knox import views as knox_views

urlpatterns = [
    path('api/auth/staff', include('knox.urls')),
    path('api/auth/staff/login', LoginStaffAPI.as_view()),
    path('api/auth/staff/user', StaffAPI.as_view()),
    path('api/auth/staff/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/auth/staff/register_test', RegisterStaffAPI.as_view()),
]