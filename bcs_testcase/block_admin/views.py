from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from block_manage.models import Transaction


def main(request):
    if not request.user.is_authenticated:
        context = {'form': LoginForm()}
        return render(request, 'login.html', context)
    if not request.user.is_staff:
        raise Http404

    return render(request, 'admin.html', {"transactions": Transaction.objects.all()})


def change_tx_description(request, txid):
    tx = Transaction.objects.filter(tx_id=txid)
    if not tx or request.method != "POST":
        raise Http404
    new_description = request.POST['description']
    tx[0].description = new_description
    tx[0].save()
    return redirect('/admin')


def admin_login(request):
    if request.method != "POST":
        raise Http404
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin')
    else:
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form})


def admin_logout(request):
    http_ref = request.META.get("HTTP_REFERER", "/")
    logout(request)
    return HttpResponseRedirect(http_ref)




