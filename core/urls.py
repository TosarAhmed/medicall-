from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .forms import LoginForm
from .views import userlogin, verify_otp

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    # path('login/', auth_views.LoginView.as_view(template_name = 'core/login.html', authentication_form = LoginForm), name = 'login'),
    path('login/', userlogin, name = 'login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-otp/', verify_otp, name='verify-otp'),

]