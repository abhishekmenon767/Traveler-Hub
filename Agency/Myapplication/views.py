
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect


from .models import Agencys, Packages, Reservation, StaffProfiles, Userprofiles
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime





# Create your views here.

# homepage
def homepage(request):
    view_package = Packages.objects.all()
    a = Agencys.objects.all()
    print('AAAAAAAA',view_package)
    all_location = Agencys.objects.values_list('location', 'id').distinct().order_by()
    if request.method == "POST":
        try:
            print(request.POST)
            data1 = Packages.objects.filter(location=int(request.POST['search_location']))
            rr = []


            for each_reservation in Reservation.objects.all():
                if str(each_reservation.check_in) < str(request.POST['cin']) and str(each_reservation.check_out) < str(
                        request.POST['cout']):
                    pass
                elif str(each_reservation.check_in) > str(request.POST['cin']) and str(
                        each_reservation.check_out) > str(request.POST['cout']):
                    pass
                else:
                    rr.append(each_reservation.package.id)

            package = Packages.objects.all().filter(capacity__gte=int(request.POST['capacity'])).exclude(
                id__in=rr)
            if len(package) == 0:
                messages.warning(request, "Sorry No Packages Are Available on this time period")
            data = {'view_package':view_package,'packages': package, 'all_location': all_location,'data1':data1 ,'flag': True}
            return render(request, 'index.html', data)
        except Exception as e:
            messages.error(request, e)
            return render(request, 'index.html', {'all_location': all_location,'view_package':view_package,'a':a,'agency':agency})


    else:

        data = {'all_location': all_location,'view_package':view_package,'a':a}
        response = render(request, 'index.html', data)
    return HttpResponse(response)


def aboutpage(request):
    return HttpResponse(render(request, 'about.html'))


# contact page
def contactpage(request):
    return HttpResponse(render(request, 'contact.html'))



def user_sign_up(request):
    if request.method == "POST":
        user_name = request.POST['username']

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.warning(request, "Password didn't matched")
            return redirect('userloginpage')

        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request, "Username Not Available")
                return redirect('userloginpage')
        except:
            pass

        new_user = User.objects.create_user(username=user_name, password=password1)
        new_user.is_superuser = False
        new_user.is_staff = False
        new_user.save()
        messages.success(request, "Registration Successfull")
        return redirect("userloginpage")
    return HttpResponse('Access Denied')



def staff_sign_up(request):
    if request.method == "POST":
        user_name = request.POST['username']

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.success(request, "Password didn't Matched")
            return redirect('staffloginpage')
        try:
            if User.objects.all().get(username=user_name):
                messages.warning(request, "Username Already Exist")
                return redirect("staffloginpage")
        except:
            pass

        new_user = User.objects.create_user(username=user_name, password=password1)
        new_user.is_superuser = False
        new_user.is_staff = True
        new_user.save()
        messages.success(request, " Staff Registration Successfull")
        return redirect("staffloginpage")
    else:
        return HttpResponse('Access Denied')



def user_log_sign_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pswd']

        user = authenticate(username=email, password=password)
        try:
            if user.is_staff:
                messages.error(request, "Incorrect username or Password")
                return redirect('staffloginpage')
        except:
            pass

        if user is not None:
            login(request, user)
            request.session['id'] = user.id
            messages.success(request, "successful logged in")
            print("Login successfull")
            return redirect('homepage')
        else:
            messages.warning(request, "Incorrect username or password")
            return redirect('userloginpage')

    response = render(request, 'user/userlogsign.html')
    return HttpResponse(response)



def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        messages.success(request, "Logged out successfully")
        print("Logged out successfully")
        return redirect('homepage')
    else:
        print("logout unsuccessfull")
        return redirect('userloginpage')



def staff_log_sign_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                return redirect('staffpanel')
        except:
            print("NOT WORKING")
            messages.success(request, "Incorrect username or password")
            return redirect('staffloginpage')
    response = render(request, 'staff/stafflogsign.html')
    return HttpResponse(response)

@login_required(login_url='/staff')
def panel(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')

    packages = Packages.objects.all()
    a = Agencys.objects.all()
    total_packages = len(packages)
    available_packages = len(Packages.objects.all().filter(status='1'))
    reserved = len(Reservation.objects.all())

    #agency = Agencys.objects.values_list('location', 'id').distinct().order_by()

    response = render(request, 'staff/panel.html',
                      {'reserved': reserved, 'packages': packages, 'total_packages': total_packages,
                       'available': available_packages,'a':a})
    return HttpResponse(response)



@login_required(login_url='/staff')
def edit_package(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    if request.method == 'POST' and request.user.is_staff:
        print(request.POST)
        old_package = Packages.objects.all().get(id=int(request.POST['packageid']))
        package = Packages.objects.filter(location_id=request.POST.get('location'))
        old_package.package_type = request.POST['packagetype']
        old_package.capacity = int(request.POST['capacity'])
        old_package.price = int(request.POST['price'])
        old_package.package = package

        old_package.package_number = int(request.POST['packagenumber'])

        old_package.save()
        messages.success(request, "Package Details Updated Successfully")
        return redirect('staffpanel')
    else:

        package_id = request.GET['packageid']
        package = Packages.objects.all().get(id=package_id)
        response = render(request, 'staff/editpackage.html', {'package': package})
        return HttpResponse(response)



@login_required(login_url='/staff')
def add_new_package(request):
    if request.user.is_staff == False:
        return HttpResponse('Access Denied')
    if request.method == "POST":
        total_package = len(Packages.objects.all())
        new_package = Packages()

        new_package.packagenumber = total_package + 1
        new_package.package_type = request.POST['packagetype']
        new_package.capacity = int(request.POST['capacity'])
        new_package.status = request.POST['status']
        new_package.price = request.POST['price']
        new_package.location_id = int(request.POST.get('agency'))

        new_package.save()
        messages.success(request, "New Package Added Successfully")

    return redirect('staffpanel')



@login_required(login_url='/user')
def book_package_page(request):
    package = Packages.objects.all().get(id=int(request.GET['packageid']))
    return HttpResponse(render(request, 'user/bookpackage.html', {'package': package}))



@login_required(login_url='/user')
def book_package(request):
    if request.method == "POST":

        package_id = request.POST['package_id']

        package = Packages.objects.all().get(id=package_id)
        # for finding the reserved packages on this time period for excluding from the query set
        for each_reservation in Reservation.objects.all().filter(package=package):
            if str(each_reservation.check_in) < str(request.POST['check_in']) and str(each_reservation.check_out) < str(
                    request.POST['check_out']):
                pass
            elif str(each_reservation.check_in) > str(request.POST['check_in']) and str(
                    each_reservation.check_out) > str(request.POST['check_out']):
                pass
            else:
                messages.warning(request, "Sorry This Package is unavailable for Booking")
                return redirect("homepage")

        current_user = request.user
        total_person = int(request.POST['person'])
        booking_id = str(package_id) + str(datetime.datetime.now())

        reservation = Reservation()
        package_object = Packages.objects.all().get(id=package_id)
        package_object.status = '2'

        user_object = User.objects.all().get(username=current_user)

        reservation.guest = user_object
        reservation.package = package_object
        person = total_person
        reservation.check_in = request.POST['check_in']
        reservation.check_out = request.POST['check_out']

        reservation.save()

        messages.success(request, "Congratulations! Booking Successfull")

        return redirect("homepage")
    else:
        return HttpResponse('Access Denied')


@login_required(login_url='/staff')
def view_package(request):
    package_id = request.GET['packageid']
    package = Packages.objects.all().get(id=package_id)

    reservation = Reservation.objects.all().filter(package=package)
    return HttpResponse(render(request, 'staff/viewpackage.html', {'package': package, 'reservations': reservation}))




@login_required(login_url='/user')
def user_bookings(request):
    if request.user.is_authenticated == False:
        return redirect('userloginpage')
    user = User.objects.all().get(id=request.user.id)
    print(f"request user id ={request.user.id}")
    bookings = Reservation.objects.all().filter(guest=user)
    if not bookings:
        messages.warning(request, "No Bookings Found")
    return HttpResponse(render(request, 'user/mybookings.html', {'bookings': bookings}))


@login_required(login_url='/staff')
def add_new_location(request):
    if request.method == "POST" and request.user.is_staff:
        location = request.POST['new_city']
        state = request.POST['new_state']
        country = request.POST['new_country']

        agency = Agencys.objects.all().filter(location=location, state=state)
        if agency:
            messages.warning(request, "Sorry City at this Location already exist")
            return redirect("staffpanel")
        else:
            new_agency = Agencys()
            new_agency.location = location
            new_agency.state = state
            new_agency.country = country
            new_agency.save()
            messages.success(request, "New Location Has been Added Successfully")
            return redirect("staffpanel")

    else:
        return HttpResponse("Not Allowed")


# for showing all bookings to staff
@login_required(login_url='/staff')
def all_bookings(request):
    bookings = Reservation.objects.all()
    if not bookings:
        messages.warning(request, "No Bookings Found")
    return HttpResponse(render(request, 'staff/allbookings.html', {'bookings': bookings}))


def delete_package(request,pk):
    agncy_del = Agencys.objects.get(id=pk)
    agncy_del.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('staffpanel')


def delete_full_package(request,pk):
    pack_del = Packages.objects.get(id=pk)
    pack_del.delete()
    messages.success(request, "Deleted Successfully")
    return redirect('staffpanel')

@login_required(login_url='/user')
def payment(request):
    return HttpResponse(render(request, 'user/payment.html'))


@login_required(login_url='/user')
def reset_password(request):
    if request.method == 'POST':
        # Retrieve the user by username or email
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.get(username=username)

        # Set the new password
        new_password = request.POST['new_password']
        user.set_password(new_password)
        user.save()

        # Display a success message
        messages.success(request, "Password changed please login")
        return render(request, 'user/userlogsign.html')

    # Render the password reset form
    user1 = User.objects.filter(id=request.user.id)
    return render(request, 'user/reset_password.html',{'user':user1})


@login_required(login_url='/staff')
def staffreset_password(request):
    if request.method == 'POST':
        # Retrieve the user by username or email
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.get(username=username)

        # Set the new password
        new_password = request.POST['new_password']
        user.set_password(new_password)
        user.save()

        # Display a success message
        messages.success(request, "Password changed please login")
        return render(request, 'staff/stafflogsign.html')

    # Render the password reset form
    user1 = User.objects.filter(id=request.user.id)
    return render(request, 'staff/staffreset_password.html',{'user':user1})



@login_required(login_url='/user')
def userprofile(request):
    if request.user.is_authenticated == False:
        return redirect('userloginpage')

    user1 = User.objects.filter(id=request.user.id)
    return render(request, 'user/userprofile.html', {'user': user1})



def staffprofile(request):
    user1 = User.objects.filter(id=request.user.id)
    return render(request, 'staff/staffprofile.html', {'user': user1})

@login_required(login_url='/user')
def profile_upload(request):
    if request.method == 'POST':
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n4']
        e = request.POST['n5']
        f = request.POST['n6']
        q = Userprofiles.objects.get(id=request.session.get('id'))
        data = Userprofiles.objects.create(username1=q,firstname=b,lastname=c,email=d,phone=e,adharnumber=f)
        data.save()
        user1 = User.objects.filter(id=request.user.id)
        return render(request, 'user/userprofile.html', {'user': user1})