from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from houserent.models import FlatsAvailable,Flat,Booking#,Booked
from .forms import UserRegistrationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.db.models import Sum

from django.core.paginator import Paginator




# Create your views here.
def index (request):
    first=FlatsAvailable.objects.latest('id')
    latests=FlatsAvailable.objects.all().exclude(id=first.id)
    ads=FlatsAvailable.objects.all
    p=Paginator(FlatsAvailable.objects.all(),2)
    page=request.GET.get('page')
    flats=p.get_page(page)
    return render(request, 'index.html',{"ads":ads,'latest':latests,'first':first,'flats':flats})

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
        messages.error(request,'Logged out Sucessfully')
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
        images=request.FILES['flat_image']
        post=FlatsAvailable(uid=request.user,title=title,description=description,price=price,location=location,bedroom=bedroom,livingroom=livingroom,bathroom=bathroom,kitchen=kitchen,contact_number=contact_number,images=images)
        post.save()
        return redirect('index')
    else:
         return render(request, 'postad.html',{})
    

def adDetail(request,slugs,id):
    data=FlatsAvailable.objects.get(slugs=slugs)

    others=FlatsAvailable.objects.exclude(id=id)

    if request.method=="POST":
        flat_id=request.POST['flat-id']
        user_id=request.user
        print(flat_id)
        flat_instance=FlatsAvailable.objects.get(id=flat_id)
        res=Booking(user=user_id,flat=flat_instance)
        res.save()
        return redirect('index')
    

    return render(request,'adviews.html',{'d':data,'o':others})

# Search Flat
def search_flat(request):
        if request.method == "POST":
            search= request.POST['search']
            flats=FlatsAvailable.objects.filter(title__contains=search)
            return render(request, 'search_flat.html',{'search':search, 'flats':flats})
        else:
            return render(request, 'search_flat.html',{})
        
# profile page
@login_required
def profile(request):
    post_history=FlatsAvailable.objects.filter(uid=request.user)
    Bookings=Booking.objects.filter(user=request.user)
    # pagination
    paginator_d=Paginator(post_history,10)
    pg_num_d=request.GET.get('page')
    pg_obj_d=paginator_d.get_page(pg_num_d)

    res_msg=""
    if request.method == 'POST':
     
        
            try:
                booking_id = request.POST['book-id']
                res = Booking.objects.get(id=booking_id)
                res.delete()
                res_msg="booking success"
                return redirect(request.path)
            except Exception as e:
                flat_id=request.POST['flat-id']
                res=FlatsAvailable.objects.get(id=flat_id)
                res.delete()
                res_msg="flat post deleted"
                return redirect(request.path)


    return render(request,'profile.html',{'rd':pg_obj_d,'bookings':Bookings,"msg":res_msg})


#price filter
def home(request):
    # Retrieve all flats initially
    flats = FlatsAvailable.objects.all()

    # Handle form submission
    if request.method == 'GET':
        # Get filter parameters from the form
        price_min = request.GET.get('priceMin')
        price_max = request.GET.get('priceMax')
        location = request.GET.get('location')

        # Apply filters to the queryset
        if price_min:
            flats = flats.filter(price__gte=price_min)
        if price_max:
            flats = flats.filter(price__lte=price_max)
        if location:
            flats = flats.filter(location__icontains=location)

    return render(request, '.html', {'flats': flats})

#Bookings
# def booking(request):
#     if request.user.is_authenticated==True:
#         flat_id=request.Bookings.id
#         user=Booked.object.filter(flat_id=flat_id,status='r')
#         if request.method=='POST':
#             flatid=request.POST['flat_id']
#             Booked.objects.filter(id=flatid).delete()
#         return render(request,'profile.html',{'flat_id':flat_id,'user':user})
#     else:
#         return redirect('profile')

def flat_detail(request, flat_id):
    flat = Flat.objects.get(pk=flat_id)
    user = request.user
    # booking_status = Booking.objects.filter(user=user, flat=flat).exists()

    context = {
        'flat': flat,
        # 'booking_status': booking_status,
    }

    return render(request, 'flat_detail.html', context)

def book_flat(request, flat_id):
    flat = Flat.objects.get(pk=flat_id)
    user = request.user

    if not Booking.objects.filter(user=user, flat=flat).exists():
        Booking.objects.create(user=user, flat=flat, status='Already Booked')
        # Add any additional logic or processing here
    
    return redirect('flat_detail', flat_id=flat_id)