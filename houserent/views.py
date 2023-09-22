from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from houserent.models import FlatsAvailable
from .forms import UserRegistrationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.db.models import Sum


# Create your views here.
def index (request):
    return render(request, 'index.html',{})

def register(request):
    if request.method == 'POST':
         form = UserRegistrationForm(request.POST)
         if form.is_valid():
             form.save()
             user = form.cleaned_data.get('username')
             messages.success(request, 'Account was created for ' + user)
             return redirect('login')
    else:
        form=UserRegistrationForm()

    context = {'form':form}
    
    return render(request, 'register.html',context)
    
def user_login(request):
    
    if request.method == "POST":
        username = request.POST['Username']
        password = request.POST['Password']
        user_data = authenticate(username=username, password=password)
        if user_data is  None:
            messages.error(request,'Incorrect Username or Password');
        if user_data is not None:
           

            login(request, user_data)
            uname=user_data.get_username
            messages.success(request,'Logged in Sucessfully');
            return redirect('index')
            

    if request.user.is_authenticated==True:
        return redirect('index')
        
    else:
        return render(request, 'login.html')  


@login_required
def logout_user(request):
    if User.is_authenticated:
        logout(request)
        messages.error(request,'Logout in Sucessfully');
        return redirect('index')        

@login_required
def postad(request):
    if request.method=="POST":
        title=request.POST['ad_title']
        description= request.POST['description']
        price=request.POST['rent']
        location=request.POST['location']
        bedroom=request.POST['bedroom']
        livingroom=request.POST['living_room']
        bathroom=request.POST['bathroom']
        kitchen=request.POST['kitchen']
        contact_number=request.POST['contact_number']
        images=request.POST['flat_image']
        post=FlatsAvailable(title=title,description=description,price=price,location=location,bedroom=bedroom,livingroom=livingroom,bathroom=bathroom,kitchen=kitchen,contact_number=contact_number,images=images)
        post.save()
        return redirect('index')
    else:
         return render(request, 'postad.html',{})