from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Wallet, Transaction
from portfolio.models import Project

@login_required
def wallet_dashboard(request):
    # Safe query: fetch or create wallet
    wallet, created = Wallet.objects.get_or_create(
        user=request.user,
        defaults={'balance': 0, 'locked_balance': 0}
    )

    # Projects where user is assigned and status is paid
    projects = Project.objects.filter(
        assigned_designer=request.user,
        status='paid'
    ).order_by('-id')

    # Transactions linked to this user
    transactions = Transaction.objects.filter(user=request.user).order_by('-created')

    return render(request, 'wallets/wallet.html', {
        'wallet': wallet,
        'transactions': transactions,
        'projects': projects
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wallet

@login_required
def withdraw_funds(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    if request.method == "POST":
        amount = float(request.POST.get("amount", 0))
        if amount > 0 and wallet.balance >= amount:
            wallet.balance -= amount
            wallet.save()
            # यहाँ आप Transaction भी बना सकते हो
            return redirect('wallet_dashboard')
    return render(request, 'wallets/withdraw.html', {'wallet': wallet})
