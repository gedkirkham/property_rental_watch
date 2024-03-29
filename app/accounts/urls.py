from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import AddressCreateView, AddressUpdateView, ProfileView, SignUp

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', SignUp.as_view(), name="signup"),
    path('profile/', ProfileView.as_view(), name="profile"),
]