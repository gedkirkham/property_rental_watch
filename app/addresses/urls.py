from django.urls import path, include

from .views import AddressDetailView

app_name = 'addresses'

urlpatterns = [
    path('<int:pk>/', AddressDetailView.as_view(), name='address_detail'),
]
