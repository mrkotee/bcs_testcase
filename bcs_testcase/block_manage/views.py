from django.shortcuts import render, redirect
from django.http import Http404
from .models import Transaction
from .bcs_connection import RPCConnect, CoinManage
from django.conf import settings


def main(request):

    return render(request, "index.html", {"transactions": Transaction.objects.all()})


def new_transaction(request):
    if request.method != "POST":
        raise Http404
    rpc = RPCConnect(settings.BCS_IP, settings.BCS_USER, settings.BCS_PSW)
    addr_to = rpc.get_new_addr()
    network = CoinManage.create_bcs_network()
    signed_tx = CoinManage.create_signed_tx(network, settings.BCS_WALLET, addr_to, 1e8, [settings.BCS_WALLET_PRV])
    sended_tx_id = rpc.send_singned_tx(signed_tx.as_hex())
    new_tx = Transaction(sended_tx_id)
    new_tx.save()
    return redirect("/")


def update_transactions(request):
    if request.method != "POST":
        raise Http404

    txs = CoinManage.get_wallet_transactions(settings.BCS_WALLET)
    for tx in txs:
        if not Transaction.objects.filter(tx_id=tx):
            new_tx = Transaction(tx)
            new_tx.save()
    return redirect("/")


def get_transaction(request, txid):
    tx = Transaction.objects.filter(tx_id=txid)
    if not tx:
        raise Http404
    return render(request, "transaction_page.html", {'tx': tx[0]})
