"""Agency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import Myapplication.views as views



urlpatterns = [
    path('', views.homepage,name="homepage"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home', views.homepage,name="homepage"),
    path('package_search',views.homepage),
    path('about', views.aboutpage,name="aboutpage"),
    path('contact', views.contactpage,name="contactpage"),
    path('user', views.user_log_sign_page,name="userloginpage"),
    path('user/login', views.user_log_sign_page,name="userloginpage"),
    path('user/bookings', views.user_bookings,name="dashboard"),
    path('user/book-package', views.book_package_page,name="bookpackagepage"),
    path('user/book-package/book', views.book_package,name="bookpackage"),
    path('user/signup', views.user_sign_up,name="usersignup"),
    path('staff/', views.staff_log_sign_page,name="staffloginpage"),
    path('staff/login', views.staff_log_sign_page,name="staffloginpage"),
    path('staff/signup', views.staff_sign_up,name="staffsignup"),
    path('logout', views.logoutuser,name="logout"),
    path('staff/panel', views.panel,name="staffpanel"),
    path('staff/allbookings', views.all_bookings,name="allbookigs"),
    # path('staff/panel/staffprofile', views.staffprofile,name="staffprofile"),
    # path('staff/panel/Staffprofilepage', views.Staffprofilepage,name="Staffprofilepage"),
    # path('staff/profile_upload_staff', views.profile_upload_staff,name="profile_upload_staff"),
    path('staff/panel/add-new-location', views.add_new_location,name="addnewlocation"),
    path('staff/panel/edit-package', views.edit_package),
    path('staff/deletestaff/<int:pk>', views.delete_package),
    path('staff/panel/add-new-package', views.add_new_package,name="addpackage"),
    path('staff/panel/edit-package/edit', views.edit_package),
    path('staff/<int:pk>', views.delete_full_package),
    path('staff/panel/view-package', views.view_package),
    path('user/payment.html', views.payment),
    path('user/reset_password',views.reset_password,name="reset_password"),
    path('staff/staffreset_password', views.staffreset_password, name="staffreset_password"),
    path('user/userprofile',views.userprofile,name="userprofile"),
    path('user/profile_upload',views.profile_upload,name="profile_upload"),
    path('staff/staffprofile', views.staffprofile, name="staffprofile"),
    path('admin/', admin.site.urls),




]