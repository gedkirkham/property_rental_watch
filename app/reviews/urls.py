from django.urls import path, include

from .views import ActivateReview, ReviewCreateView, ReviewDetailView

app_name = 'reviews'

urlpatterns = [
    path('new/', ReviewCreateView.as_view(), name='review_create'),
    path('<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('activate/<uidb64>/<reviewb64>/<token>/',
         ActivateReview.as_view(), name='review_activate'),
]
