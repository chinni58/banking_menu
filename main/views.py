from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Account
import random

def home(request):
    return render(request, 'home.html')

# ✅ Create Account
def create_account(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            message = 'User already exists'
        else:
            user = User.objects.create_user(username=username, password=password)
            acc_no = str(random.randint(100000000000, 999999999999))
            Account.objects.create(user=user, account_number=acc_no)
            message = f'Account created! Account No: {acc_no}'
    return render(request, 'create_account.html', {'message': message})

# ✅ Deposit / Withdraw / Balance / Transfer
def transaction(request):
    message = ''
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username')
        amount = float(request.POST.get('amount', 0))
        receiver = request.POST.get('receiver')

        try:
            user = User.objects.get(username=username)
            acc = Account.objects.get(user=user)
        except:
            return render(request, 'transaction.html', {'message': 'User not found!'})

        if action == 'deposit':
            acc.balance += amount
            acc.save()
            message = f'Deposited ₹{amount}. New balance: ₹{acc.balance}'
        elif action == 'withdraw':
            if acc.balance >= amount:
                acc.balance -= amount
                acc.save()
                message = f'Withdrawn ₹{amount}. Remaining: ₹{acc.balance}'
            else:
                message = 'Insufficient balance!'
        elif action == 'transfer':
            try:
                r_user = User.objects.get(username=receiver)
                r_acc = Account.objects.get(user=r_user)
                if acc.balance >= amount:
                    acc.balance -= amount
                    r_acc.balance += amount
                    acc.save()
                    r_acc.save()
                    message = f'Transferred ₹{amount} to {receiver}'
                else:
                    message = 'Not enough funds'
            except:
                message = 'Receiver not found!'
        elif action == 'check':
            message = f'Your balance is ₹{acc.balance}'
    return render(request, 'transaction.html', {'message': message})

# ✅ Login / Logout / Change Password
def security(request):
    message = ''
    if 'login' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            message = 'Logged in successfully!'
        else:
            message = 'Invalid credentials'
    elif 'logout' in request.POST:
        logout(request)
        message = 'Logged out successfully!'
    elif 'change' in request.POST:
        username = request.POST.get('username')
        old = request.POST.get('old_password')
        new = request.POST.get('new_password')
        user = authenticate(username=username, password=old)
        if user:
            user.set_password(new)
            user.save()
            message = 'Password changed successfully!'
        else:
            message = 'Incorrect old password'
    return render(request, 'security.html', {'message': message})
