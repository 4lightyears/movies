from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.signup_account, name='signup_account'),
    path('logout/', views.logout_account, name='logout_account'),
    path('login/', views.login_account, name='login_account'),
]
