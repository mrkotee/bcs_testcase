from django.urls import path
from .views import main, admin_login, admin_logout, change_tx_description

urlpatterns = [
    path('', main),
    path('login/', admin_login),
    path('logout/', admin_logout),
    path('change_desc/<str:txid>/', change_tx_description),
]