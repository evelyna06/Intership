from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def Home(request):
 return render(request,'Home.html')

def loguin(request):
    if request.method =='GET':
       return render (request,'loguin.html',{
          'form':AuthenticationForm()
       })
    else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            messages.error(request, "User or password incorrect")
            return render(request,'loguin.html')
        else:
            login(request,user)
            return redirect('task')


def signup(request):
    if request.method =='GET':
       return render (request,'signup.html',{
          'form':UserCreationForm
       })
    else:
        if request.POST['password1']== request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('task')
            except IntegrityError:
                return render (request,'signup.html',{
                    'form':UserCreationForm,
                    "error":'username already exist'
                })
        return render(request,'signup.html',{
            'form':UserCreationForm,
            "error" : 'password dont not match'
        })

def task(request):
   return render(request,'task.html')

def signout(request):
    logout(request)
    return redirect('Home')


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Esto asi mantengo la sesion abierta despues del cambio 
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was updated successfully ✅")
            return redirect("task")  # O a donde quieras redirigirlo
        else:
            messages.error(request, "Correct the errors in the form ❌")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})

