from django.urls import path

from .views import AddressDetailView, AddressCreateView, AddressLookupView

app_name = 'addresses'

urlpatterns = [
    path('<int:pk>/', AddressDetailView.as_view(), name='address_detail'),
    path('lookup/', AddressLookupView.as_view(), name='address_lookup'),
    path('create/', AddressCreateView.as_view(), name='address_create'),
]
