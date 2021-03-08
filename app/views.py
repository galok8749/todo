from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as loginUser, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        tasks = TODO.objects.filter(user=user).order_by('priority')
        return render(request, 'app/index.html', context={'form':form, 'tasks': tasks})



def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            'form':form
        }
        return render(request, 'app/login.html', context=context)
    else:
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
             
            if user is not None:
                loginUser(request, user)
                return redirect('home')
        else:
            form = AuthenticationForm()
            context = {
                'form':form
            }
            return render(request, 'app/login.html', context=context)



def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request, 'app/signup.html', context=context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request, 'app/signup.html', context=context)


@login_required(login_url='login')
def add_task(request):
    if request.user.is_authenticated:
        form = TODOForm(request.POST)
        user = request.user
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            return redirect('home')
        else:
            return render(request, 'app/index.html', context={'form':form})


def signout(request):
    logout(request)
    return redirect('login')

def delete_task(request, id):
    TODO.objects.get(pk=id).delete()
    return redirect('home')

def change_task(request, id, status):
    task = TODO.objects.get(pk=id)
    task.status = status
    task.save()
    return redirect('home')