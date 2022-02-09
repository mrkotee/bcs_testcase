from django.urls import path
from .views import main, update_transactions, new_transaction, get_transaction

urlpatterns = [
    path('', main),
    path('update_txs/', update_transactions),
    path('new_tx/', new_transaction),
    path('tx/<str:txid>', get_transaction),
    ]