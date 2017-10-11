from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            #navigateToIndex
    return render(request,'order/register.html',{'form':form})


