# function corresponds to urls
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as auth_logout, authenticate


from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.http import Http404
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .forms import vehicheForm, profileForm, userForm, UserProfileUpdateForm, RegisterForm, requestRideForm, orderSearchForm, driverSearchForm
from .models import Profile, Vehicle, Order, DriverToVehicle

rideOpen = 0
rideConfirmed = 1
rideCompleted = 2


# register
def regView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username):
                msg = "user is existed"
            else:
                form.save()
                user = User.objects.get(username=username)
                userProfile = Profile(user=user)
                userProfile.save()
                return redirect("/user/login/")
    else:
        form = RegisterForm()
    return render(request, "usr/register.html", {'form': form})


##personal index
def index(request):
    return render(request, "usr/index.html", {"name": request.session.get('uname')})


# log in
def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    request.session['status'] = True
                    request.session['uname'] = username
                    request.session.set_expiry(300)

                return redirect("/user/index/")
            else:
                msg = "wrong password"
        else:
            msg = "user is not existed"
    return render(request, "usr/login.html", locals())


# logout
def logout(request):
    auth_logout(request)
    return redirect("/user/login/")


# driver register
@login_required
def regDriver(request):
    if request.method == 'POST':
        form = vehicheForm(request.POST)
        # select
        profile = Profile.objects.get(user=request.user.id)
        if (profile.is_driver == True):
            context = {'prompt': "You have been a driver!"}
            return render(request, "usr/index.html", context)
        if form.is_valid():
            # profile table
            profile.is_driver = True
            profile.save()

            # vechicle table
            plate_num = form.cleaned_data.get('plate_num')
            vehicle_type = form.cleaned_data.get('vehicle_type')
            max_capacity = form.cleaned_data.get('max_capacity')
            special_info = form.cleaned_data.get('special_info')
            vehicle = Vehicle(plate_num=plate_num, vehicle_type=vehicle_type, max_capacity=max_capacity,
                              special_info=special_info)
            vehicle.save()

            # DriverToVehicle table
            user = User.objects.get(pk=request.user.id)
            driverToVehicle = DriverToVehicle(driver=user, vehicle=vehicle)
            driverToVehicle.save()

            context = {'prompt': "You are a driver now!"}
            return render(request, "usr/index.html", context)
    else:
        form = vehicheForm()
    return render(request, "usr/regDriver.html", {'form': form})

@login_required
def viewOrEditeDriver(request):
    profile = Profile.objects.get(user=request.user.id)
    # update user information
    if request.method == 'POST':
        # update profile
        uForm = UserProfileUpdateForm(request.POST)
        vForm = vehicheForm(request.POST)
        pForm = profileForm()
        if uForm.is_valid():
            email = uForm.cleaned_data.get('email')
            User.objects.filter(pk=request.user.id).update(email=email)

        if vForm.is_valid():
            plate_num = vForm.cleaned_data.get('plate_num')
            vehicle_type = vForm.cleaned_data.get('vehicle_type')
            max_capacity = vForm.cleaned_data.get('max_capacity')
            special_info = vForm.cleaned_data.get('special_info')
            vehicle = DriverToVehicle.objects.get(driver=request.user.id).vehicle
            if (profile.is_driver == True):
                Vehicle.objects.filter(pk=vehicle.id).update(plate_num=plate_num, vehicle_type=vehicle_type,
                                                             max_capacity=max_capacity, special_info=special_info)
        uForm = userForm(instance=request.user)
        context = {
            # 'uForm': uForm,
            # 'vForm': vForm,
            # 'pForm': pForm
            'prompt':"Update successfully!"
        }
        return render(request, 'usr/index.html', context)

    # view information
    else:
        uForm = userForm(instance=request.user)
        vForm = vehicheForm()
        pForm = profileForm()
        if (profile.is_driver == True):
            vehicle = DriverToVehicle.objects.get(driver=request.user.id).vehicle
            vForm = vehicheForm(instance=vehicle)
            pForm = profileForm(instance=Profile.objects.get(user=request.user.id))
        context = {
            'uForm': uForm,
            'vForm': vForm,
            'pForm': pForm
        }
    return render(request, 'usr/profile.html', context)

def driverQuit(request):
    vehicle = DriverToVehicle.objects.get(driver=request.user.id).vehicle
    Vehicle.objects.filter(pk=vehicle.id).delete()
    DriverToVehicle.objects.filter(driver=request.user.id).delete()
    Profile.objects.filter(user=request.user.id).update(is_driver=False)

    context = {'prompt': "You are not a driver anymore !"}
    return render(request, "usr/index.html", context)

@login_required
def requestRide(request):
    if request.method == 'POST':
        form = requestRideForm(request.POST)
        if form.is_valid():
            arrival_time = form.cleaned_data.get('arrival_time')
            destination = form.cleaned_data.get('destination')
            capacity = form.cleaned_data.get('capacity')
            vehicle_type = form.cleaned_data.get('vehicle_type')
            is_shared = form.cleaned_data.get('is_shared')
            special_info = form.cleaned_data.get('special_info')


            user = User.objects.get(pk=request.user.id)
            order = Order(arrival_time=arrival_time, destination=destination, capacity=capacity,
                          vehicle_type=vehicle_type, is_shared=is_shared, special_info=special_info, owner=user)
            order.save()

            context = {'prompt': "You have requested a ride !"}
            return render(request, "usr/index.html", context)
    else:
        form = requestRideForm()
    return render(request, "usr/requestRide.html", {'form': form})

@login_required
def viewRide(request):
    orderOwnOpen = list(Order.objects.filter(owner=request.user, status=rideOpen))
    orderOwnConfirm = list(Order.objects.filter(owner=request.user, status=rideConfirmed))
    orderShareOpen = list(Order.objects.filter(sharer=request.user, status=rideOpen))
    orderShareConfirm = list(Order.objects.filter(sharer=request.user, status=rideConfirmed))
    orderDriver = list(Order.objects.filter(driver=request.user, status=rideConfirmed))
    context = {
               'ownerOpen': orderOwnOpen,
               'ownerConfirm': orderOwnConfirm,
               'shareOpen': orderShareOpen,
               'shareConfirm': orderShareConfirm,
               'driver': orderDriver
               }
    return render(request, "usr/viewRide.html", context)

def updateRide(request, ride_id):
    order = Order.objects.get(pk=ride_id)
    if request.method == 'POST':
        form = requestRideForm(request.POST)
        if form.is_valid():
            arrival_time = form.cleaned_data.get('arrival_time')
            destination = form.cleaned_data.get('destination')
            capacity = form.cleaned_data.get('capacity')
            vehicle_type = form.cleaned_data.get('vehicle_type')
            is_shared = form.cleaned_data.get('is_shared')
            special_info = form.cleaned_data.get('special_info')

            Order.objects.filter(pk=ride_id).update(arrival_time=arrival_time, destination=destination, capacity=capacity,
                          vehicle_type=vehicle_type, is_shared=is_shared, special_info=special_info)
            context = {'prompt': "You have updated the ride !"}
            return render(request, "usr/index.html", context)
    else:
        form = requestRideForm(instance=order)
    return render(request, 'usr/updateRide.html', {'form': form})

#order review
def viewOrder(request):
    orders_owner = Order.objects.filter(owner = request.user.id)
    orders_sharer = Order.objects.filter(sharer = request.user.id)
    driver_owner = {}
    driver_sharer = {}
    # for ride in orders_owner:
    #     vechToDriver = DriverToVehicle.objects.get(driver = ride.driver)
    #     vech = vechToDriver.vehicle
    #     driver_owner.appened(vech)
    # print(driver_owner)
    dic = {}
    dic['list_owner'] = orders_owner
    dic['list_sharer'] = orders_sharer
    #dic['driver_owner'] = driver_owner
    #dic['len_owner'] = len(dic['list_owner'])
    return  render (request,"usr/viewOrder.html", dic)

#driver mode
def driverMode(request):
    user = Profile.objects.get(user=request.user.id)
    #print(driver)
    if(user.is_driver):
        return  render (request,"usr/driverMode.html",{"name":request.session.get('uname')})
    else:
        return redirect("/user/regDriver/")
        #print(person)

#view ride of driver
def viewDriverOrder(request):
    orders = Order.objects.filter(driver=request.user.id).all()
    return render(request,"usr/viewDriverOrder.html",{'list':orders})

#search for Order
def joinOrderSearch(request):
    context = {}
    if(request.method == 'POST'):
        form = orderSearchForm(request.POST)
        if form.is_valid():
            dest = form.cleaned_data['destination']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            number = form.cleaned_data['number']
            print(number)
            print(start)
            print(end)
            print(dest)
            orders = Order.objects.filter(capacity__lte=number, destination = dest, status = 0,arrival_time__range=(start,end), 
                                            is_shared = True).exclude(owner = request.user.id).exclude(sharer = request.user.id)
            context['orders']=orders
            print(orders)
            return render(request, 'usr/joinOrder.html', {'orders':orders})
    else :
        form = orderSearchForm()
        return render(request, 'usr/joinOrderSearch.html', {'form':form})

#join an order
def joinOrder(request,ride_id):
    ride = Order.objects.filter(pk=ride_id).first()
    ride.sharer.add(request.user)
    ride.capacity += 1
    ride.save()
    print(ride)
    context = {'prompt': "You have joined the ride !"}
    return render(request, "usr/index.html", context)
    
#search for Order by driver
def driverSearch(request):
    context = {}
    if(request.method == 'POST'):
        form = driverSearchForm(request.POST)
        if form.is_valid():
            vech_type = form.cleaned_data['vechicle_type']
            start =  form.cleaned_data['start']
            end = form.cleaned_data['end']

            vehicle = DriverToVehicle.objects.get(driver = request.user.id).vehicle
            max_capacity = vehicle.max_capacity
            orders = Order.objects.filter( vehicle_type = vech_type, status = 0,capacity__lte = max_capacity,
                                        arrival_time__range=(start,end),).exclude(owner = request.user.id).exclude(sharer = request.user.id)
            print(orders)
            context['orders']=orders
            print(orders)
            return render(request, 'usr/driverConfirm.html', {'orders':orders})
    else :
        form = driverSearchForm()
        return render(request, 'usr/driverSearch.html', {'form':form})

#confirm driver
def driverConfirm(request, ride_id):
    ride = Order.objects.filter(pk=ride_id).first()
    ride.status = '1'
    ride.driver = User.objects.get(pk=request.user.id)
    ride.save()
    e_list = []
    e_list.append(ride.owner.email)
    #print(e_list)
    sharer = ride.sharer.all()
    for person in sharer:
        e_list.append(person.email)
    
    
    context = "Thank you for waiting. Your order has been confrimed.\n" + \
                "Here are the information of your order:\n"+ \
                'Arrival at: ' + str(ride.arrival_time) + '\n'+\
                'Destination: ' + ride.destination + '\n'+\
                'Driver name: ' + request.user.username + '\n'+\
                'Vehicle type: ' + ride.vehicle_type + '\n'+\
                'Sharers: '
    for person in sharer:
        context += str(person.username) + ' '

    send_mail(
        subject = 'Confirmation of your order',
        message = context,
        from_email = 'xxxxxx@163.com',
        recipient_list = e_list,
        fail_silently = False
    )

    context = {'prompt': "You have confrimed the ride !"}
    return render(request, "usr/driverMode.html", context)

def driverCompleted(request, ride_id):
    ride = Order.objects.filter(pk=ride_id).first()
    ride.status='2'
    ride.save()
    context = {'prompt': "You have completed the ride !"}
    return render(request, "usr/driverMode.html", context) 

def deleteOwner(request,ride_id):
    ride=Order.objects.get(pk=ride_id)
    ride.delete()
    context = {'prompt': "You have cancled the ride as an owner!"}
    return render(request, "usr/index.html", context) 

def deleteSharer(request,ride_id):
    ride=Order.objects.get(pk=ride_id)
    ride.sharer.remove(request.user)
    ride.capacity -= 1
    ride.save()
    context = {'prompt': "You have cancle the ride as a sharer!"}
    return render(request, "usr/index.html", context) 
