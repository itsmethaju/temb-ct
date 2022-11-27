import email
from itertools import product
import uuid
from urllib import request
from django.shortcuts import render, redirect
from . import forms, models
#from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
#from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
#from datetime import datetime,timedelta,date
# from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import razorpay
import http.client
import random
from django.contrib.auth import authenticate, login
from .helpers import send_forget_password_mail,subscriber_send_forget_password_mail
from math import ceil
from django.contrib.auth.models import User, auth

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import datetime
from datetime import timedelta
from datetime import datetime as dt
today = datetime.date.today()
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver
from django.contrib.sessions.models import Session
from .models import UserSession



@receiver(user_logged_out)
def sig_user_logged_out(sender, user, request, **kwargs):
    if is_admin(request.user):
        pass
    elif is_creator(request.user):
        user.creator.last_logout = dt.now()
        user.creator.save()
    elif is_customer(request.user):
        user.customer.last_logout = dt.now()
        user.customer.save()
    else:
        pass



razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))


def test(request):
    return render(request, 'landing/Home.html')


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'main_ui/index.html')


def home(request):
    return render(request, 'first-page.html')

# for showing signup/login button for admin(by sumit)


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'adminclick.html')


# for showing signup/login button for doctor(by sumit)
def createrclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'createrclick.html')


# for showing signup/login button for patient(by sumit)
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'costomerclick.html')


def admin_signup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request, 'reg.html', {'form': form})


############################################################################################################
def creater_signup_view(request):

    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        profile = request.FILES.get('profile')

        if password == confirm_password:
            if models.User.objects.filter(username=username).exists():
                messages.info(request, 'User Name Already Created')
                return redirect('creatorsignup')
            else:
                if models.User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Already Exist')
                    return redirect('creatorsignup')
                elif models.Creator.objects.filter(mobile=mobile).exists():
                    messages.info(request, 'Mobile Number Already Exist')
                    return redirect('creatorsignup')
                else:

                    user = models.User.objects.create_user(
                        username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                    user.save()
                    date = dt.now()
                    data = models.Creator(
                        user=user, mobile=mobile, address=address, gender=gender, email=email, profile=profile,date=date)
                    data.save()
                    my_creater_group = Group.objects.get_or_create(
                        name='CREATOR')
                    profile_obj = models.Profile.objects.create(user=user)
                    profile_obj.save()
                    my_creater_group[0].user_set.add(user)
                    # code for login user will come here
                    our_user = authenticate(
                        username=username, password=password)
                    if our_user is not None:

                        login(request, user)

                        otp = str(random.randint(1000, 9999))
                        profile = models.Creator(
                            user=user, mobile=mobile, email=email, otp=otp, address=address, profile=profile)
                        profile.save()
                        send_masge_otp(otp, mobile)
                        send_email_otp(otp, email)

                        request.session['mobile'] = mobile
                        request.session['email'] = email
                        return redirect('otp')
                #        return redirect('/')

        else:
            messages.info(request, "password and confirm password mismatch!")
            return redirect('creatorsignup')

    return render(request, 'reg/creater-reg.html')


def send_email_otp(otp, email):
    otp = otp
    email = email

    print(otp, email)
    conn = http.client.HTTPSConnection("api.msg91.com")
    payload = "{\n  \"to\": [\n{\n\"name\":\"mathewsoninfotech\",\n\"email\":   \""+email+"\" \n }\n  ],\n  \"from\": {\n\"name\":\"Mathewsoninfotech\",\n    \"email\": \"thajudheen@mathewsoninfotech.com\" },\n  \"domain\": \"mstestndemo.mathewsoninfotech.com\", \r\n\"mail_type_id\": \"1\",				\r\n\"template_id\":			\"MST-DIGITAL\",\n  \"variables\": {\n    \"VAR1\": \"" + \
        otp+"\" ,\"VAR2\": \""+email+"\" ,\"VAR3\": \""+otp + \
            "\" ,\"VAR4\": \"hello\" ,\n    	\"VAR5\":\"hi\"  },\n  \"authkey\": \"375863AOJUpBOm52625d40baP1\"\n}"
#    payload = "{\n  \"to\": [\n{\n\"name\": "+ name1 +",\n\"email\": \"thajudheenac12@gmail.com\"\n }\n  ],\n  \"from\": {\n\"name\": \"mathewsoninfotech\",\n    \"email\": \"thajudheen@mathewsoninfotech.com\"\n  },\n  \"domain\": \"mstestndemo.mathewsoninfotech.com\", \r\n\"mail_type_id\": \"1\",        \r\n\"template_id\":        \"mathewsoninfotech_thank_you\",\n  \"variables\": {\n    \"VAR1\": \"'name'\" ,\n      \"VAR2\":\"'ms infotech'\"  },\n  \"authkey\": \"375863AOJUpBOm52625d40baP1\"\n}"

    print(payload)

    headers = {
        'Content-Type': "application/JSON",
        'Accept': "application/json"
    }

    conn.request("POST", "/api/v5/email/send", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))
    return redirect('/')


def send_masge_otp(otp, mobile):
    print(otp, mobile)

    conn = http.client.HTTPSConnection("api.msg91.com")

    payload = "{\n  \"flow_id\": \"62ecb8eff4eadf36ca2f1808\",\n  \"sender\": \"AOLBLR\",\n  \"short_url\": \"1 (On) or 0 (Off)\",\n  \"mobiles\": \"91" + \
        mobile+"\",\n  \"otp\": \""+otp+"\"\n}"

    headers = {
        'authkey': "375863AOJUpBOm52625d40baP1",
        'content-type': "application/JSON"
    }

    conn.request("POST", "/api/v5/flow/", payload, headers)

    res = conn.getresponse()
    data = res.read()
    print(payload)
    print(data.decode("utf-8"))



def creatorlogin(request):
    if request.method == 'POST':
        userinput = request.POST['username']
        try:
            username = User.objects.get(email=userinput).username
        except User.DoesNotExist:
            username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request,"Login successfull")
            return redirect('afterlogin')
        else:
            messages.error(request,'Invalid credentials, Please check username/email or password. ')
    return render(request, 'reg/creater-login.html')

        

# Cut login
########################################################################################################
@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    UserSession.objects.filter(user=kwargs.get('user')).delete()



def customerlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('afterlogin')
        messages.info(request, 'User Login Failed Pleas Try Again ..')
    return render(request, 'reg/customer-login.html' )


def customr_signup_view(request):

    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        profile = request.FILES.get('profile')

        if password == confirm_password:
            if models.User.objects.filter(username=username).exists():
                messages.info(request, 'User Name Already Created')
                return redirect('customersignup')
            else:
                if models.User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Already Exist')
                    return redirect('customersignup')
                elif models.Customer.objects.filter(mobile=mobile).exists():
                    messages.info(request, 'Mobile Number Already Exist')
                    return redirect('customersignup')
                else:

                    user = models.User.objects.create_user(
                        username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                    user.save()
                    data = models.Customer(
                        user=user, mobile=mobile, email=email)
                    data.save()
                    my_customer_group = Group.objects.get_or_create(
                        name='CUSTOMER')
                    profile_obj = models.Profile.objects.create(user=user)
                    profile_obj.save()

                    my_customer_group[0].user_set.add(user)
                    # code for login user will come here
                    our_user = authenticate(
                        username=username, password=password)
                    if our_user is not None:

                        login(request, user)

                        otp = str(random.randint(1000, 9999))
                        profile = models.Customer(
                            user=user, mobile=mobile, email=email, otp=otp)
                        profile.save()
                        send_masge_otp(otp, mobile)
                        send_email_otp(otp, email)
                        request.session['mobile'] = mobile
                        request.session['email'] = email
                        return redirect('coustomer_otp')
                #        return redirect('/')

        else:
            messages.info(request, "password and confirm password mismatch!")
            return redirect('customersignup')

    return render(request, 'reg/customer-reg.html')


@login_required(login_url='creatorlogin')
def otp(request):
    email = request.session['email']
    mobile = request.session['mobile']

    context = {'mobile': mobile, 'email': email}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = models.Creator.objects.filter(email=email).first()

        if otp == profile.otp:

            return redirect('afterlogin')
        else:
            print('Wrong')
            user = models.User.objects.filter(email=email).first()

            user.delete()
            context = {'message': 'Wrong OTP',
                       'class': 'danger', 'mobile': mobile}
            return render(request, 'otp.html', context)

    return render(request, 'otp.html', context)


def coustomer_otp(request):
    email = request.session['email']
    mobile = request.session['mobile']
    context = {'mobile': mobile, 'email': email}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = models.Customer.objects.filter(email=email).first()

        if otp == profile.otp:
            return redirect('afterlogin')
        else:
            print('Wrong')

            context = {'message': 'Wrong OTP',
                       'class': 'danger', 'mobile': mobile}
            return render(request, 'otp.html', context)

    return render(request, 'otp.html', context)
###############################################################################################

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def is_creator(user):

    return user.groups.filter(name='CREATOR').exists()


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


@login_required()
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('dashbordadmin')
    elif is_creator(request.user):
        status = models.OrderItem.objects.all().filter(
            user_id=request.user.id)

        accountapproval = models.Creator.objects.all().filter(
            user_id=request.user.id, status=True)


        if status:

            user=request.user.username

            return redirect('creator-dashboard', username=user)
        
        else:
            return redirect('plans')
      

    elif is_customer(request.user):
        accountapproval = models.Customer.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('customer-dashboard')
        else:
            return redirect('customer_dashboard')

    else:
        return redirect('dashbordadmin')


def logout(request):
    return render(request, 'first-page.html')
#@ subscribers logout ##########
def subscribers_logout(request):
    return redirect('customerlogin')
# End#################

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):

    return render(request, 'home.html')


# sub

@login_required(login_url='creatorlogin')
def plans(request):
    plans = models.Creator_SubscribationPlan.objects.all()
    return render(request, 'pricing-style-2.html', {'plans': plans})

@login_required(login_url='creatorlogin')
def add_item(request, pk):# subscribation
    product = models.Creator_SubscribationPlan.objects.get(pk=pk)
    item = models.OrderItem.objects.filter(user=request.user)
    # create order item

    order_item, created = models.OrderItem.objects.get_or_create(
        product=product,
        expires_in=dt.now().date() + timedelta(days=product.duration),
        user=request.user,
        ordered=False,
    )

    # get query set of order object of user
    order_qs = models.Subscription.objects.filter(
        user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(pk=pk).exists():

            order_item.save()
            messages.info(request, "added quantity item")
            return redirect('checkout', pk=pk)

        else:
            order.items.add(order_item)
            messages.info(request, "item add to cart")
            return redirect("checkout", pk=pk)
    else:
        ordered_date = timezone.now()
        order = models.Subscription.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "item added to cart")
        return redirect('checkout', pk=pk)


@login_required(login_url='creatorlogin')
def checkout(request, pk):
    planDetail = models.Creator_SubscribationPlan.objects.get(pk=pk)
    order_amount =planDetail.plane_price + planDetail.Gst
    return render(request, 'checkout.html', {'plan': planDetail, 'payment_allow': 'allow','price':order_amount})


@login_required(login_url='creatorlogin')
def payment(request):
    try:
        mobile = models.Creator.objects.get(user=request.user)
        order = models.Subscription.objects.get(user=request.user)
        order_amount = order.get_total_price()
        order_currency = "INR"
        order_receipt = order.ordered_id
        razorpay_order = razorpay_client.order.create(
            dict(
                amount=order_amount * 100,
                currency=order_currency,
                receipt=order_receipt,
                payment_capture="0",
            )
        )
        print(razorpay_order["id"])
        order.razorpay_order_id = razorpay_order["id"]
        order.save()
        print('it should render the summary page ')
        return render(
            request,
            "paymentsummaryrazorpay.html",
            {
                "order": order,
                "order_id": razorpay_order["id"],
                "orderId": order.ordered_id,
                "final_price": order_amount,
                "razorpay_merchant_id": settings.RAZORPAY_ID,
                "mobile":mobile
            },
        )
    except models.Subscription.DoesNotExist:
        print("order not fount")
        return HttpResponse("404 error")

# Cancel


def pay_cancel(request):
    return render(request, 'cancel.html')


@csrf_exempt
def handlerequest(request, id):
    if request.method == "POST":
        try:
            payment_id = request.POST.get("razorpay_payment_id", "")
            order_id = request.POST.get("razorpay_order_id", "")
            signature = request.POST.get("razorpay_signature", "")
            print(payment_id, order_id, signature)
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            try:
                order_db = models. Subscription.objects.get(
                    razorpay_order_id=order_id)
                print("Order Found")
            except:
                print("Order Not found")
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            print("Working............")
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result == None:
                print("Working Final Fine............")
                amount = order_db.get_total_price()
                amount = amount * 100  # we have to pass in paisa
                payment_status = razorpay_client.payment.capture(
                    payment_id, amount)
                if payment_status is not None:
                    print(payment_status)
                    order_db.ordered = True
                    order_db.save()

                    print("Payment Success")

                    request.session[
                        "order_complete"
                    ] = "Your Order is Successfully Placed, You will receive your order within 5-7 working days"
                    return render(request, "Invoice.html", {"order": order_db, "payment_status": payment_status, })
                else:
                    print("Payment Failed")
                    order_db.ordered = False
                    order_db.save()
                    request.session[
                        "order_failed"
                    ] = "Unfortunately your order could not be placed, try again!"
                    return redirect("/")
            else:
                order_db.ordered = False
                order_db.save()
                return render(request, "paymentfailed.html")
        except:
            creator = models.Creator.objects.get(user=request.user)
            creator.status = True
            creator.save()
            user=request.user.username
            plan = models.OrderItem.objects.get(user=request.user)
            plan.ordered=True
            plan.save()

            return redirect('creator-dashboard', username=user)
# creator area    ===============================================================


################################ Creator Current Plane ##################

def current_plane(request):
    
    ct = models.Creator.objects.filter(user=request.user)
    plane = models.OrderItem.objects.filter(user=request.user)
    plans = models.Creator_SubscribationPlan.objects.all()
    payment = models.Subscription.objects.get(user=request.user)

    return render(request,'creator_admin/currentplane.html', {'plane':plane,'ct':ct,'plans':plans,'pay':payment})


def activate_plan(request,id):

    obj = models.OrderItem.objects.get(id=id)
    obj.delete()
    creator = models.Creator.objects.get(user=request.user)
    creator.status = False
    creator.save()
    payment = models.Subscription.objects.filter(user=request.user)
    payment.delete()
    return redirect('current_plane')



def profileview(request):
    ct = models.Creator.objects.filter(user=request.user)
    me = models.Creator.objects.get(user=request.user)
    return render(request,'creator_admin/profile.html',{'me':me,'ct':ct})






@login_required(login_url='creatorlogin')

def creator_dashboard_view(request,username):
    thisuser = (models.User.objects.filter(username=username))
    if len(thisuser) != 0:
        thisuser = thisuser[0]
        video = models.CreatorAddVideo.objects.filter(
            user=thisuser).order_by('-user_id')
        category = models.VideoCaregory.objects.filter(
            user=thisuser).order_by('-user_id')
        posts = models.Creator.objects.filter(
            user=thisuser).order_by('-user_id')
        baner = models.Coverphoto.objects.filter(
            user=thisuser).order_by('-user_id')
        # video=models.CreatorAddVideo.objects.filter(user=thisuser).order_by('-user_id')
        series = models.PlayLists.objects.filter(
            user=thisuser).order_by('-user_id')
        return render(request, 'home.html', {'posts': posts, 'thisuser': thisuser, 'baner': baner, 'series': series, 'category': category,'video':video, 'title': thisuser.username})
    else:
        return redirect('home')

# user session allow

# @receiver(user_logged_in)
# def remove_other_session(sender,user,request,**kwargs):

#     Session.objects.filter(usersession_user=user).delete()

#     request.Session.save()
#     UserSession.objects.get_or_create(
#         user =user,
#         session_id=request.session.session_key
#     )







@login_required(login_url='creatorlogin')
def videosingleview(request, id):

    video = models.CreatorAddVideo.objects.get(id=id)

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
    ip = get_client_ip(request)
    u = models.ViewUser(user=ip)
    print(ip)
    result = models.ViewUser.objects.filter(Q(user__icontains=ip))
    if len(result) == 1:
        print("uesr exist")
    elif len(result) > 1:
        print("user exist")
    else:
        u.save()
        print("uesr is unique")
    count = models.ViewUser.objects.all().count()
    print("totel user is ", count)
    return render(request, 'single_video.html', {'vd': video, 'count': count})


@login_required(login_url='creatorlogin')
def crt(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.CreatorAddVideo.objects.filter(user=request.user).count()
    series = models.PlayLists.objects.filter(user=request.user).count()
    return render(request, 'creator_admin/index.html', {'ct': me,'vd':video,'se':series })


@login_required(login_url='creatorlogin')
def crt_addvideo(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.CreatorAddVideo.objects.filter(user=request.user)
    form = forms.VideoForm(request.POST, request.FILES, user=request.user)
    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('crt_addvideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.VideoForm(user=request.user)

    return render(request, 'creator_admin/add-video.html', {'form': form, 'vd': video, 'ct': me, })
# =================================================================================================


@login_required(login_url='creatorlogin')
def crt_addvideolink(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.CreatorAddVideo.objects.filter(user=request.user)
    form = forms.VideoLinkForm(request.POST, request.FILES,user=request.user)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('crt_addvideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.VideoLinkForm(user=request.user)

    return render(request, 'creator_admin/add-videolink.html', {'form': form, 'vd': video, 'ct': me, })
# ===================================================


@login_required(login_url='creatorlogin')
def videolist(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.CreatorAddVideo.objects.filter(user=request.user)
    return render(request, 'creator_admin/list_display.html', {'vd': video, 'ct': me, })


@login_required(login_url='creatorlogin')
def deleteVideo(request, id):

    obj = models.CreatorAddVideo.objects.get(id=id)
    obj.delete()
    return redirect('videolist')
    # return render(request,'creator_admin/list_display.html')
########################################################################################################################################################################


@login_required(login_url='creatorlogin')
def videoupdate(request, id):
    video = models.CreatorAddVideo.objects.filter(user=request.user)
    me = models.Creator.objects.filter(user=request.user)
    try:
        obj = models.CreatorAddVideo.objects.get(id=id)
    except models.Creator.DoesNotExist:
        return HttpResponse("invalid Viseos!")
    if request.method == "POST":
        form = forms.VideoForm(data=request.POST,
         instance=obj,user=request.user)
        if form.is_valid():
            video = form.save(commit=False)

            if 'image' in request.FILES:
                video.image = request.FILES['image']
            elif 'videofile' in request.FILES:
                video.videofile = request.FILES['videofile']
            video.save()
            return redirect('videolist')
        else:
            print('errors')
    else:
        video = models.CreatorAddVideo.objects.filter(user=request.user)
        form = forms.VideoForm(instance=obj,user=request.user)
        me = models.Creator.objects.filter(user=request.user)
    return render(request, 'creator_admin/updatevideo.html', {'vd': video, 'form': form,'ct': me, })

############################################################################
@login_required(login_url='creatorlogin')
def videoupdatelink(request, id):
    video = models.CreatorAddVideo.objects.filter(user=request.user)
    me = models.Creator.objects.filter(user=request.user)
    try:
        obj = models.CreatorAddVideo.objects.get(id=id)
    except models.Creator.DoesNotExist:
        return HttpResponse("invalid Viseos!")
    if request.method == "POST":
        form = forms.VideoLinkForm(data=request.POST,
         instance=obj,user=request.user)
        if form.is_valid():
            video = form.save(commit=False)

            if 'image' in request.FILES:
                video.image = request.FILES['image']
            elif 'videofile' in request.FILES:
                video.videofile = request.FILES['videofile']
            video.save()
            return redirect('videolist')
        else:
            print('errors')
    else:
        video = models.CreatorAddVideo.objects.filter(user=request.user)
        form = forms.VideoLinkForm(instance=obj,user=request.user)
        me = models.Creator.objects.filter(user=request.user)
    return render(request, 'creator_admin/updatevideo.html', {'vd': video, 'form': form,'ct': me, })
###########################################################################################################################################################################


@login_required(login_url='customerlogin')
def profile(request, username):
    ct =models.Creator.objects.filter(user=request.user)
    thisuser = (models.User.objects.filter(username=username))
    if len(thisuser) != 0:
        thisuser = thisuser[0]
        category = models.VideoCaregory.objects.filter(
            user=thisuser).order_by('-user_id')
        posts = models.Creator.objects.filter(
            user=thisuser).order_by('-user_id')
        baner = models.Coverphoto.objects.filter(
            user=thisuser).order_by('-user_id')
        # video=models.CreatorAddVideo.objects.filter(user=thisuser).order_by('-user_id')
        series = models.PlayLists.objects.filter(
            user=thisuser).order_by('-user_id')
        return render(request, 'home.html', {'posts': posts, 'thisuser': thisuser, 'baner': baner, 'series': series, 'category': category, 'ct':ct, 'title': thisuser.username})
    else:
        return redirect('home')


def videocategory(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.VideoCaregory.objects.filter(user=request.user)
    form = forms.VideoCaregoryForm(request.POST, request.FILES)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('videocategory')
        else:
            messages.info(request, "category is not added ,try again ")
    else:
        form = forms.VideoCaregoryForm()

    return render(request, 'creator_admin/video_category.html', {'form': form, 'vd': video, 'ct': me, })




@login_required(login_url='creatorlogin')
def deletecaregory(request, id):
    obj = models.VideoCaregory.objects.get(id=id)
    obj.delete()
    return redirect('videocategory')
    # return render(request,'creator_admin/category_list.html')


@login_required(login_url='creatorlogin')
def updatecategory(request, id):
    me = models.Creator.objects.filter(user=request.user)
    video = models.VideoCaregory.objects.filter(user=request.user)
    obj = models.VideoCaregory.objects.get(id=id)
    form = forms.VideoCaregoryForm(
        request.POST, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('videocategory')
    return render(request, 'creator_admin/updatecategory.html', {'form': form, 'obj': obj, 'vd': video, 'ct': me, })




############################################################################################################################

@login_required(login_url='customerlogin')
def sub_add_item(request, pk):
    product = models.CreatorAddVideo.objects.get(pk=pk)

    # create order item
    order_item, created = models.SubOrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    # get query set of order object of user
    order_qs = models.SubSubscription.objects.filter(
        user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(pk=pk).exists():

            order_item.save()
            messages.info(request, "added quantity item")
            return redirect('sub_checkout', pk=pk)

        else:
            order.items.add(order_item)
            messages.info(request, "item add to cart")
            return redirect("sub_checkout", pk=pk)
    else:
        ordered_date = timezone.now()
        order = models.SubSubscription.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "item added to cart")
        return redirect('sub_checkout', pk=pk)


@login_required(login_url='customerlogin')
def sub_checkout(request, pk):
    planDetail = models.CreatorAddVideo.objects.get(pk=pk)

    return render(request, 'customer/customer_checkout.html', {'plan': planDetail, 'payment_allow': 'allow'})


@login_required(login_url='customerlogin')
def sub_payment(request):
    try:
        order = models.SubSubscription.objects.get(user=request.user)

        order_amount = order.get_total_price()
        order_currency = "INR"
        order_receipt = order.ordered_id
        razorpay_order = razorpay_client.order.create(
            dict(
                amount=order_amount * 100,
                currency=order_currency,
                receipt=order_receipt,
                payment_capture="0",
            )
        )
        print(razorpay_order["id"])
        order.razorpay_order_id = razorpay_order["id"]
        order.save()
        print('it should render the summary page ')
        return render(
            request,
            "customer/customer_paymentsummaryrazorpay.html",
            {
                "order": order,
                "order_id": razorpay_order["id"],
                "orderId": order.ordered_id,
                "final_price": order_amount,
                "razorpay_merchant_id": settings.RAZORPAY_ID,
            },
        )
    except models.Subscription.DoesNotExist:
        print("order not fount")
        return HttpResponse("404 error")





# Cancel


def pay_cancel(request):
    return render(request, 'cancel.html')


@csrf_exempt
def sub_handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get("razorpay_payment_id", "")
            order_id = request.POST.get("razorpay_order_id", "")
            signature = request.POST.get("razorpay_signature", "")
            print(payment_id, order_id, signature)
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            try:
                order_db = models. SubSubscription.objects.get(
                    razorpay_order_id=order_id)
                print("Order Found")
            except:
                print("Order Not found")
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            print("Working............")
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result == None:
                print("Working Final Fine............")
                amount = order_db.get_total_price()
                amount = amount * 100  # we have to pass in paisa
                payment_status = razorpay_client.payment.capture(
                    payment_id, amount)
                if payment_status is not None:
                    print(payment_status)
                    order_db.ordered = True
                    order_db.save()
                    print("Payment Success")

                    request.session[
                        "order_complete"
                    ] = "Your Order is Successfully Placed, You will receive your order within 5-7 working days"
                    return render(request, "Invoice.html", {"order": order_db, "payment_status": payment_status, })
                else:
                    print("Payment Failed")
                    order_db.ordered = False
                    order_db.save()
                    request.session[
                        "order_failed"
                    ] = "Unfortunately your order could not be placed, try again!"
                    return redirect("/")
            else:
                order_db.ordered = False
                order_db.save()
                return render(request, "paymentfailed.html")
        except:

            return redirect('customer_dashboard')


@login_required(login_url='customerlogin')
def customer_dashboard(request):

    posts = models.Creator.objects.filter(user=request.user)
    baner = models.Coverphoto.objects.filter(user=request.user)
    video = models.SubOrderItem.objects.filter(
        user=request.user).order_by('-id')
    series = models.SubseriesOrderItem.objects.filter(
        user=request.user).order_by('-id')
    wish = models.Wishlist.objects.filter(user=request.user).order_by('-id')
    downloadedvideo = models.DownloadVideo.objects.filter(user=request.user).order_by('-id')
    return render(request, 'customer/customer_dash.html', {'posts': posts, 'baner': baner, 'video': video, 'wish': wish, 'series': series,'downloadedvideo':downloadedvideo})


@login_required(login_url='customerlogin')
def customer_video_det(request, id):
    video = models.SubOrderItem.objects.get(id=id)

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
    ip = get_client_ip(request)
    u = models.ViewUser(user=ip)
    print(ip)
    result = models.ViewUser.objects.filter(Q(user__icontains=ip))
    if len(result) == 1:
        print("uesr exist")
    elif len(result) > 1:
        print("user exist")
    else:
        u.save()
        print("uesr is unique")
    count = models.ViewUser.objects.all().count()
    print("totel user is ", count)
    return render(request, 'customer/single.html', {'vd': video, 'count': count})


def subscriberlist(request):
    me = models.Creator.objects.filter(user=request.user)
    list = models.SubOrderItem.objects.filter(product__user=request.user)
    

    return render(request, "creator_admin/subscrbers.html", {'list': list, 'ct': me, })


########################## Terms and conditions ####################################
def privecy(request):
    return render(request, 'privecy.html')

################################################ domnload videos ###################################
def sub_download_video(request, pk):
    video = models.SubOrderItem.objects.get(pk=pk)

    # create order item
    created = models.DownloadVideo.objects.get_or_create(
        video=video,
        user=request.user,

    )
    return redirect(request.META.get('HTTP_REFERER'))
################################################ domnload videos single View ###################################
def download_video_detail(request,pk):
    video = models.DownloadVideo.objects.get(pk=pk)
    return render(request, 'customer/download_single.html', {'vd': video})
################################################## wish list#############################

def sub_wishlist_item(request, pk):
    product = models.CreatorAddVideo.objects.get(pk=pk)

    # create order item
    order_item, created = models.Wishlist.objects.get_or_create(
        product=product,
        user=request.user,

    )
    return redirect(request.META.get('HTTP_REFERER'))

def sub_series_wishlist_item(request, pk):
    product = models.PlayLists.objects.get(pk=pk)

    # create order item
    order_item, created = models.Wishlist.objects.get_or_create(
        product=product,
        user=request.user,

    )
    return redirect(request.META.get('HTTP_REFERER'))

########################### play list ###########################

@login_required(login_url='creatorlogin')
def crt_PlalistVideo(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.PlayLists.objects.filter(user=request.user)
    form = forms.PlayListsForm(request.POST, request.FILES)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('crt_PlalistVideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.PlayListsForm()

    return render(request, 'creator_admin/crt_playlistadd.html', {'form': form, 'vd': video, 'ct': me, })


@login_required(login_url='creatorlogin')
def crt_PlalistVideolinkmode(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.PlayLists.objects.filter(user=request.user)
    form = forms.PlayListlinksForm(request.POST, request.FILES,user=request.user)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('crt_PlalistVideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.PlayListlinksForm(user=request.user)

    return render(request, 'creator_admin/crt_playlistaddlink.html', {'form': form, 'vd': video, 'ct': me, })


@login_required(login_url='creatorlogin')
def deleteVideoLIst(request, id):

    obj = models.PlayLists.objects.get(id=id)
    obj.delete()
    return redirect('videoPlaylist')
    # return render(request,'creator_admin/list_display.html')

########################### UPDATE PLAYLIST###########################
@login_required(login_url='creatorlogin')
def videoupdateList(request, id):
    me = models.Creator.objects.filter(user=request.user)
    video = models.PlayLists.objects.filter(user=request.user)
    try:
        obj = models.PlayLists.objects.get(id=id)
    except models.Creator.DoesNotExist:
        return HttpResponse("invalid Viseos!")

    if request.method == "POST":
        form = forms.PlayListsForm(
        data=request.POST, instance=obj,user=request.user)
        if form.is_valid():
            video=form.save(commit=False)
            if 'image' in request.FILES:
                video.image = request.FILES['image']
            elif 'videofile' in request.FILES:
                video.videofile = request.FILES['videofile']
            video.save()
            return redirect('videoPlaylist')
        else:
            print('form error')
    else:
        video = models.PlayLists.objects.filter(user=request.user)
        form = forms.PlayListsForm(instance=obj,user=request.user)
        me = models.Creator.objects.filter(user=request.user)
    return render(request, 'creator_admin/updateseries.html', {'form': form, 'obj': obj, 'vd': video, 'ct': me, })
#####################################UPDATE PLAYLIST LINK#########################
def videoupdateListlink(request, id):
    me = models.Creator.objects.filter(user=request.user)
    video = models.PlayLists.objects.filter(user=request.user)
    try:
        obj = models.PlayLists.objects.get(id=id)
    except models.Creator.DoesNotExist:
        return HttpResponse("invalid Viseos!")

    if request.method == "POST":
        form = forms.PlayListlinksForm(
        data=request.POST, instance=obj,user=request.user)
        if form.is_valid():
            video=form.save(commit=False)
            if 'image' in request.FILES:
                video.image = request.FILES['image']
            elif 'videofile' in request.FILES:
                video.videofile = request.FILES['videofile']
            video.save()
            return redirect('videoPlaylist')
        else:
            print('form error')
    else:
        video = models.PlayLists.objects.filter(user=request.user)
        form = forms.PlayListlinksForm(instance=obj,user=request.user)
        me = models.Creator.objects.filter(user=request.user)
    return render(request, 'creator_admin/updateseries.html', {'form': form, 'obj': obj, 'vd': video, 'ct': me, })


########################################################################

@login_required(login_url='creatorlogin')
def videoPlaylist(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.PlayLists.objects.filter(user=request.user)
    return render(request, 'creator_admin/serieslist.html', {'vd': video, 'ct': me, })


def seriessingleview(request, id):
    video = models.PlayLists.objects.get(id=id)
    series = models.Video.objects.filter(playlists=video)

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
    ip = get_client_ip(request)
    u = models.ViewUser(user=ip)
    print(ip)
    result = models.ViewUser.objects.filter(Q(user__icontains=ip))
    if len(result) == 1:
        print("uesr exist")
    elif len(result) > 1:
        print("user exist")
    else:
        u.save()
        print("uesr is unique")
    count = models.ViewUser.objects.all().count()
    print("totel user is ", count)
    return render(request, 'singleseries.html', {'vd': video, 'count': count, 'series': series})


########################### play list video ###########################

@login_required(login_url='creatorlogin')
def add_PlalistVideo(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.Video.objects.filter(user=request.user)
    form = forms.PlayListsvideoForm(request.POST, request.FILES,user=request.user)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('add_PlalistVideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.PlayListsvideoForm(user=request.user)

    return render(request, 'creator_admin/addvideoseries.html', {'form': form, 'vd': video, 'ct': me, })


@login_required(login_url='creatorlogin')
def add_PlalistVideolinkmode(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.Video.objects.filter(user=request.user)
    form = forms.PlayListsvideolinkForm(request.POST, request.FILES,user=request.user)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('add_PlalistVideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.PlayListsvideolinkForm(user=request.user)

    return render(request, 'creator_admin/addvideoserieslink.html', {'form': form, 'vd': video, 'ct': me, })


@login_required(login_url='creatorlogin')
def deleteVideoseries(request, id):

    obj = models.Video.objects.get(id=id)
    obj.delete()
    return redirect('videoserieslist')
    # return render(request,'creator_admin/list_display.html')
#######################################################################################
########################### UPDATE PLAYLIST single video###########################
@login_required(login_url='creatorlogin')
def videoupdateseries(request, id):
    me = models.Creator.objects.filter(user=request.user)
    video = models.Video.objects.filter(user=request.user)
    try:
        obj = models.Video.objects.get(id=id)
    except models.Creator.DoesNotExist:
        return HttpResponse("invalid Viseos!")

    if request.method == "POST":
        form = forms.PlayListsvideoForm(
        data=request.POST, instance=obj,user=request.user)
        if form.is_valid():
            video=form.save(commit=False)
            if 'image' in request.FILES:
                video.image = request.FILES['image']
            elif 'videofile' in request.FILES:
                video.videofile = request.FILES['videofile']
            video.save()
            return redirect('videoserieslist')
        else:
            print('form error')
    else:
        video = models.Video.objects.filter(user=request.user)
        form = forms.PlayListsvideoForm(instance=obj,user=request.user)
        me = models.Creator.objects.filter(user=request.user)
    return render(request, 'creator_admin/updateseriessingle.html', {'form': form, 'obj': obj, 'vd': video, 'ct': me, })
#####################################UPDATE PLAYLIST LINK single video link#########################
def videoupdateserieslink(request, id):
    me = models.Creator.objects.filter(user=request.user)
    video = models.Video.objects.filter(user=request.user)
    try:
        obj = models.Video.objects.get(id=id)
    except models.Creator.DoesNotExist:
        return HttpResponse("invalid Viseos!")

    if request.method == "POST":
        form = forms.PlayListsvideolinkForm(
        data=request.POST, instance=obj,user=request.user)
        if form.is_valid():
            video=form.save(commit=False)
            if 'image' in request.FILES:
                video.image = request.FILES['image']
            elif 'videofile' in request.FILES:
                video.videofile = request.FILES['videofile']
            video.save()
            return redirect('videoserieslist')
        else:
            print('form error')
    else:
        video = models.Video.objects.filter(user=request.user)
        form = forms.PlayListsvideolinkForm(instance=obj,user=request.user)
        me = models.Creator.objects.filter(user=request.user)
    return render(request, 'creator_admin/updateseriessingle.html', {'form': form, 'obj': obj, 'vd': video, 'ct': me, })


########################################################################
# def videoupdateseries(request, id):
#     me = models.Creator.objects.filter(user=request.user)
#     video = models.Video.objects.filter(user=request.user)
#     obj = models.Video.objects.get(id=id)
#     form = forms.PlayListsvideoForm(
#         request.POST, request.FILES or None, instance=obj)
#     if form.is_valid():
#         form.save()
#         return redirect('videoserieslist')
#     return render(request, 'creator_admin/addvideoseries.html', {'form': form, 'obj': obj, 'vd': video, 'ct': me, })


@login_required(login_url='creatorlogin')
def videoserieslist(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.Video.objects.filter(user=request.user)
    return render(request, 'creator_admin/videoserieslist.html', {'vd': video, 'ct': me, })


def seriesvideosingleview(request, id):

    videos = models.Video.objects.get(id=id)

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
    ip = get_client_ip(request)
    u = models.ViewUser(user=ip)
    print(ip)
    result = models.ViewUser.objects.filter(Q(user__icontains=ip))
    if len(result) == 1:
        print("uesr exist")
    elif len(result) > 1:
        print("user exist")
    else:
        u.save()
        print("uesr is unique")
    count = models.ViewUser.objects.all().count()
    print("totel user is ", count)
    return render(request, 'seriessingleview.html', {'vd': videos})


############################################################ Subscriber payment series ####################################################################################


@login_required(login_url='customerlogin')
def sub_series_add_item(request, pk):
    product = models.PlayLists.objects.get(pk=pk)

    # create order item
    order_item, created = models.SubseriesOrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    # get query set of order object of user
    order_qs = models.SubseriesSubscription.objects.filter(
        user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(pk=pk).exists():

            order_item.save()
            messages.info(request, "added quantity item")
            return redirect('sub_series_checkout', pk=pk)

        else:
            order.items.add(order_item)
            messages.info(request, "item add to cart")
            return redirect("sub_series_checkout", pk=pk)
    else:
        ordered_date = timezone.now()
        order = models.SubseriesSubscription.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "item added to cart")
        return redirect('sub_series_checkout', pk=pk)


@login_required(login_url='customerlogin')
def sub_series_checkout(request, pk):
    planDetail = models.PlayLists.objects.get(pk=pk)

    return render(request, 'customer/sub_series_checkout.html', {'plan': planDetail, 'payment_allow': 'allow'})


@login_required(login_url='customerlogin')
def sub_series_payment(request):
    try:
        order = models.SubseriesSubscription.objects.get(user=request.user)

        order_amount = order.get_total_price()
        order_currency = "INR"
        order_receipt = order.ordered_id
        razorpay_order = razorpay_client.order.create(
            dict(
                amount=order_amount * 100,
                currency=order_currency,
                receipt=order_receipt,
                payment_capture="0",
            )
        )
        print(razorpay_order["id"])
        order.razorpay_order_id = razorpay_order["id"]
        order.save()
        print('it should render the summary page ')
        return render(
            request,
            "customer/subseries_payment.html",
            {
                "order": order,
                "order_id": razorpay_order["id"],
                "orderId": order.ordered_id,
                "final_price": order_amount,
                "razorpay_merchant_id": settings.RAZORPAY_ID,
            },
        )
    except models.SubseriesSubscription.DoesNotExist:
        print("order not fount")
        return HttpResponse("404 error")

# Cancel


def pay_cancel(request):
    return render(request, 'cancel.html')


@csrf_exempt
def sub_series_handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get("razorpay_payment_id", "")
            order_id = request.POST.get("razorpay_order_id", "")
            signature = request.POST.get("razorpay_signature", "")
            print(payment_id, order_id, signature)
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }

            try:
                order_db = models. SubseriesSubscription.objects.get(
                    razorpay_order_id=order_id)
                print("Order Found")
            except:
                print("Order Not found")
                return HttpResponse("505 Not Found")
            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            print("Working............")
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result == None:
                print("Working Final Fine............")
                amount = order_db.get_total_price()
                amount = amount * 100  # we have to pass in paisa
                payment_status = razorpay_client.payment.capture(
                    payment_id, amount)
                if payment_status is not None:
                    print(payment_status)
                    order_db.ordered = True
                    order_db.save()
                    print("Payment Success")

                    request.session[
                        "order_complete"
                    ] = "Your Order is Successfully Placed, You will receive your order within 5-7 working days"
                    return render(request, "Invoice.html", {"order": order_db, "payment_status": payment_status, })
                else:
                    print("Payment Failed")
                    order_db.ordered = False
                    order_db.save()
                    request.session[
                        "order_failed"
                    ] = "Unfortunately your order could not be placed, try again!"
                    return redirect("/")
            else:
                order_db.ordered = False
                order_db.save()
                return render(request, "paymentfailed.html")
        except:

            return redirect('customer_dashboard')


@login_required(login_url='customerlogin')
def customer_series_video_det(request, id):
    video = models.SubseriesOrderItem.objects.get(id=id)

    series = models.Video.objects.filter(playlists=video.product)

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
    ip = get_client_ip(request)
    u = models.ViewUser(user=ip)
    print(ip)
    result = models.ViewUser.objects.filter(Q(user__icontains=ip))
    if len(result) == 1:
        print("uesr exist")
    elif len(result) > 1:
        print("user exist")
    else:
        u.save()
        print("uesr is unique")
    count = models.ViewUser.objects.all().count()
    print("totel user is ", count)
    return render(request, 'customer/series_cust_single.html', {'vd': video, 'count': count, 'series': series})
######################################################################################################################################


@login_required(login_url='customerlogin')
def cust_seriesvideosingleview(request, id):

    videos = models.Video.objects.get(id=id)

    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
    ip = get_client_ip(request)
    u = models.ViewUser(user=ip)
    print(ip)
    result = models.ViewUser.objects.filter(Q(user__icontains=ip))
    if len(result) == 1:
        print("uesr exist")
    elif len(result) > 1:
        print("user exist")
    else:
        u.save()
        print("uesr is unique")
    count = models.ViewUser.objects.all().count()
    print("totel user is ", count)
    return render(request, 'customer/cust_seriessingleview.html', {'vd': videos})


##################################################################################################################
def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = models.Profile.objects.filter(
            forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')

            user_obj = models.User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('creatorlogin')

    except Exception as e:
        print(e)
    return render(request, 'change-password.html', context)


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not models.User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')

            user_obj = models.User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = models.Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent. Check Your Email')
            return redirect('/forget-password/')

    except Exception as e:
        print(e)
    return render(request, 'forget-password.html')
################################# subscriber change and forget password #################################################
def Subscriber_ChangePassword(request, token):
    context = {}

    try:
        profile_obj = models.Profile.objects.filter(
            forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/Subscriber_ChangePassword/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/Subscriber_ChangePassword/{token}/')

            user_obj = models.User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('customerlogin')

    except Exception as e:
        print(e)
    return render(request, 'customer/subscriber_change-password.html', context)


def Subscriber_ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not models.User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/Subscriber_ForgetPassword/')

            user_obj = models.User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = models.Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            subscriber_send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent. Check Your Email')
            return redirect('/Subscriber_ForgetPassword/')

    except Exception as e:
        print(e)
    return render(request, 'customer/subscriber_forget-password.html')


################################ profile update########################
@login_required
def update_user(request):
    me = models.Creator.objects.filter(user=request.user)
    try:
        user_profile = models.Creator.objects.get(user=request.user)
    except models.Creator.DoesNotExist:
        return HttpResponse("invalid user_profile!")

    if request.method == "POST":
        me = models.Creator.objects.filter(user=request.user)
        update_user_form = forms.UserForm2(
            data=request.POST, instance=request.user)
        update_profile_form = forms.UserProfileForm(
            data=request.POST, instance=user_profile)

        if update_user_form.is_valid() and update_profile_form.is_valid():
            user = update_user_form.save()
            profile = update_profile_form.save(commit=False)
            profile.user = user

            if 'profile' in request.FILES:
                profile.profile = request.FILES['profile']

            elif 'coverphoto' in request.FILES:
                profile.coverphoto = request.FILES['coverphoto']
            profile.save()
            user=request.user.username


            return redirect('creator-dashboard', username=user)

        else:
            print(update_user_form.errors, update_profile_form.errors)
    else:
        update_user_form = forms.UserForm2(instance=request.user)
        update_profile_form = forms.UserProfileForm(instance=user_profile)
        me = models.Creator.objects.filter(user=request.user)
    return render(request,
                  'update_user.html',
                  {'update_user_form': update_user_form,
                      'update_profile_form': update_profile_form, 'ct': me, }
                  )


def deleteWishlist(request, id):

    obj = models.Wishlist.objects.get(id=id)
    obj.delete()
    return redirect('customer_dashboard')












##########################################################################################################################################################################

# MAIN NAVIGATION
# Dashboard
# Customers
# List of Customer
# Receipts
# Cancel And Refund
# Razorpay List
# Banned List
# Subscribers
# List of Subscribers
# Receipts
# Cancellation list
# Razorpay List
# Banner
# Add Slides
# Master
# Add Language
# Add Short films
# Series
# Add Series Category
# Add Series
# LEO Bucket
# Admin Users
# Add Admin Users
# List of Admin Users
# Access Rights/Role Creation
# Customers Login list
# Customers list

login_required(login_url='creatorlogin')

def dashbordadmin(request):
    user = models.User.objects.all().count()
    creator =models.Creator.objects.all().count()
    subscrbers =models.Customer.objects.all().count()
    video = models.CreatorAddVideo.objects.all().count()
    series = models.PlayLists.objects.all().count()
    return render(request, 'mainadmin/index.html',{'user':user,'crt':creator,'sub':subscrbers,'vd':video,'se':series})


login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def listofcreator(request):
    try :
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            searchresult = models.Creator.objects.raw('select user_id,mobile,gender from accounts_creator where date between"'+fromdate+'" and "'+todate+'"')
            creator = models.Creator.objects.all()
            return render(request, 'mainadmin/creatorlist.html', {'creator':searchresult,'fromdate':fromdate,'todate':todate})

        else:
            creator = models.Creator.objects.all()
            res =models.Subscription.objects.all()
            item =models.OrderItem.objects.all()
            return render(request, 'mainadmin/creatorlist.html', {'creator': creator})
    except:
        return redirect('listofcreator')

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def admincreatorview(request,id):
    crt = models.Creator.objects.get(user_id=id)
    res =models.Subscription.objects.get(user_id=id)
    item =models.OrderItem.objects.get(user_id=id)
    # find user current status ? 
    c = crt.user.last_login
    d = crt.last_logout
    v = d - c 
        
    print(v)
    print(d)
    print(c)
   
    return render(request,'mainadmin/detial.html',{'ct':crt,'res':res,'item':item,'v':v})

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def deleteCreator(request, id):

    obj = models.User.objects.get(id=id)
    obj.delete()
    return redirect('listofcreator')
###############################################################################################

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def receipts(request):
    try :
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            searchresult = models.OrderItem.objects.raw('select id,user_id,date,product_id from OrderItem where date between"'+fromdate+'" and "'+todate+'"')
            res =models.Subscription.objects.all()
            return render(request,'mainadmin/receipts.html',{'res':res,'item':searchresult,'fromdate':fromdate,'todate':todate})
        else:

            res =models.Subscription.objects.all()
            item =models.OrderItem.objects.all()
            return render(request,'mainadmin/receipts.html',{'res':res,'item':item})
    except :
        return redirect('receipts')

#######################################################################################################

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def rezorpaylist(request):
    try :
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            searchresult = models.Subscription.objects.raw('select id,user_id,start_date,razorpay_order_id from accounts_subscription where start_date between"'+fromdate+'" and "'+todate+'"')
        
            return render(request,'mainadmin/razorpaylist.html',{'rez':searchresult,'fromdate':fromdate,'todate':todate})
        else:
            rez= models.Subscription.objects.all()
            return render(request,'mainadmin/razorpaylist.html',{'rez':rez})
    except:
        return redirect('rezorpaylist')

########################################################################################################

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def listofsubscribers(request):
    try :
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            searchresult = models.Customer.objects.raw('select  user_id,mobile from accounts_customer where date between"'+fromdate+'" and "'+todate+'"')
        
            return render(request, 'mainadmin/subscriberslist.html', {'subscribers': searchresult,'fromdate':fromdate,'todate':todate})
        else:

            subscribers = models.Customer.objects.all()
    
            return render(request, 'mainadmin/subscriberslist.html', {'subscribers': subscribers})
    except:
        return redirect('listofsubscribers')


login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def adminsubscribersview(request,id):
    crt = models.Customer.objects.get(user_id=id)
    res =models.SubSubscription.objects.filter(user_id=id)
    item =models.SubOrderItem.objects.filter(user_id=id)
    return render(request,'mainadmin/adminsubsingle.html',{'ct':crt,'res':res,'item':item})


login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def deletesubscribers(request, id):

    obj = models.User.objects.get(id=id)
    obj.delete()
    return redirect('listofsubscribers')

###############################################################################################

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def subreceipts(request):
    try :
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            searchresult = models.SubOrderItem.objects.raw('select  id,user_id,date,product_id from accounts_suborderitem where date between"'+fromdate+'" and "'+todate+'"')
        
            return render(request, 'mainadmin/subreceipts.html', {'item': searchresult,'fromdate':fromdate,'todate':todate})
        else:

            res =models.SubSubscription.objects.all()
            item =models.SubOrderItem.objects.all()
            return render(request,'mainadmin/subreceipts.html',{'res':res,'item':item})
    except:
        return redirect('subreceipts')

#######################################################################################################

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def subrezorpaylist(request):
    try :
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            searchresult = models.SubSubscription.objects.raw('select  id,user_id,start_date,razorpay_order_id from accounts_subsubscription where start_date between"'+fromdate+'" and "'+todate+'"')
        
            return render(request, 'mainadmin/subrazorpaylist.html', {'rez': searchresult,'fromdate':fromdate,'todate':todate})
        else:
            rez= models.SubSubscription.objects.all()
            return render(request,'mainadmin/subrazorpaylist.html',{'rez':rez})
    except:
        return redirect('subrezorpaylist')
########################################################################################################

login_required(login_url='creatorlogin')

def admin_addvideo(request):

    video = models.CreatorAddVideo.objects.filter(user=request.user)
    form = forms.VideoForm(request.POST, request.FILES,user=request.user)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('admin_addvideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.VideoForm(user=request.user)

    return render(request, 'mainadmin/addvideo.html', {'form': form, 'vd': video, })
# =================================================================================================


login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def admin_addvideolink(request):

    video = models.CreatorAddVideo.objects.filter(user=request.user)
    form = forms.VideoLinkForm(request.POST, request.FILES,user=request.user)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('admin_addvideolink')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.VideoLinkForm(user=request.user)

    return render(request, 'mainadmin/videolinkmode.html', {'form': form, 'vd': video, })
################################################################################################

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def admin_videolist(request):

    video = models.CreatorAddVideo.objects.filter(user=request.user)
    return render(request, 'mainadmin/list_display.html', {'vd': video, })


login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def admin_deleteVideo(request, id):

    obj = models.CreatorAddVideo.objects.get(id=id)
    obj.delete()
    return redirect('admin_videolist')
    # return render(request,'creator_admin/list_display.html')
########################################################################################################################################################################

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def admin_videoupdate(request, id):

    video = models.CreatorAddVideo.objects.filter(user=request.user)
    obj = models.CreatorAddVideo.objects.get(id=id)
    form = forms.VideoForm(request.POST, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('admin_videolist')
    return render(request, 'mainadmin/add-video.html', {'form': form, 'obj': obj, 'vd': video, })

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def allVideolist(request):
    video = models.CreatorAddVideo.objects.all()
    return render(request,'mainadmin/allvideo.html',{'vd':video})
###########################################################################################################################################################################

# seeris ##################################################################################

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def admin_PlalistVideo(request):

    video = models.Video.objects.filter(user=request.user)
    form = forms.PlayListsvideoForm(request.POST, request.FILES,user=request.user)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('add_PlalistVideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.PlayListsvideoForm(user=request.user)

    return render(request, 'mainadmin/add_videoseries.html', {'form': form, 'vd': video, })


login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def admin_PlalistVideolinkmode(request):

    video = models.Video.objects.filter(user=request.user)
    form = forms.PlayListsvideolinkForm(request.POST, request.FILES,user=request.user)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('add_PlalistVideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.PlayListsvideolinkForm(user=request.user)

    return render(request, 'mainadmin/add_videoserieslink.html', {'form': form, 'vd': video, })


login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def admin_SeriesVideo(request):

    video = models.PlayLists.objects.filter(user=request.user)
    form = forms.PlayListsForm(request.POST, request.FILES,user=request.user)
    if request.method == 'POST':

        if form.is_valid(): 
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('crt_PlalistVideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.PlayListsForm(user=request.user)

    return render(request, 'mainadmin/adminseries.html', {'form': form, 'vd': video, })

login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def admin_serieslinkmode(request):

    video = models.PlayLists.objects.filter(user=request.user)
    form = forms.PlayListlinksForm(request.POST, request.FILES)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('crt_PlalistVideo')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.PlayListlinksForm()

    return render(request, 'mainadmin/adminserieslink.html', {'form': form, 'vd': video, })




#################################################################################
def admin_signup_view(request):
    form = forms.AdminSigupForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminslist')
    return render(request, 'mainadmin/addadmin.html', {'form': form})
login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def adminslist(request):

    users = User.objects.filter(groups__name__in=['ADMIN'])
    return render(request,'mainadmin/adminlistm.html',{'admin':users})
##################################################################################
login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def deleteadmin(request, id):

    obj = models.User.objects.get(id=id)
    obj.delete()
    return redirect('adminslist')
################################################################################



login_required(login_url='creatorlogin')
@user_passes_test(is_admin)
def see_users(request):
    userlist = models.User.objects.all()
    return render(request,'mainadmin/customer-login-list.html',{'user':userlist})

################################################################################
def morevideo(request, id):
    posts = models.Creator.objects.filter(user=request.user)
    baner = models.Coverphoto.objects.filter(user=request.user)
    video = models.VideoCaregory.objects.filter(id=id)
    return render(request, 'morevideo.html', {'video': video, 'posts': posts, 'baner': baner})


############################################################################################################################
def adminvideocategory(request):

    video = models.VideoCaregory.objects.filter(user=request.user)
    form = forms.VideoCaregoryForm(request.POST, request.FILES)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('adminvideocategory')
        else:
            messages.info(request, "category is not added ,try again ")
    else:
        form = forms.VideoCaregoryForm()

    return render(request,'mainadmin/add_category.html', {'form': form, 'vd': video,  })


@login_required(login_url='creatorlogin')
def admincaregory_list(request):

    video = models.VideoCaregory.objects.filter(user=request.user)
    return render(request,'mainadmin/list_category.html', {'vd': video })


@login_required(login_url='creatorlogin')
def admindeletecaregory(request, id):
    obj = models.VideoCaregory.objects.get(id=id)
    obj.delete()
    return redirect('admincaregory_list')
    # return render(request,'creator_admin/category_list.html')

def adminupdatecategory(request, id):

    video = models.VideoCaregory.objects.filter(user=request.user)
    obj = models.VideoCaregory.objects.get(id=id)
    form = forms.VideoCaregoryForm(
        request.POST, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('caregory_list')
    return render(request, 'mainadmin/add_category.html', {'form': form, 'obj': obj, 'vd': video })

##########################################################################################################################
@login_required(login_url='creatorlogin')
def deleteVideoseries(request, id):

    obj = models.Video.objects.get(id=id)
    obj.delete()
    return redirect('videoserieslist')
    # return render(request,'creator_admin/list_display.html')


def adminvideoupdateseries(request, id):
    me = models.Creator.objects.filter(user=request.user)
    video = models.Video.objects.filter(user=request.user)
    obj = models.Video.objects.get(id=id)
    form = forms.PlayListsvideoForm(
        request.POST, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('videoserieslist')
    return render(request, 'creator_admin/addvideoseries.html', {'form': form, 'obj': obj, 'vd': video, 'ct': me, })


@login_required(login_url='creatorlogin')
def videoserieslist(request):
    me = models.Creator.objects.filter(user=request.user)
    video = models.Video.objects.filter(user=request.user)
    return render(request, 'creator_admin/videoserieslist.html', {'vd': video, 'ct': me, })

###############################################################################################################################################
def add_Plan(request):
    
    plan = models.Creator_SubscribationPlan.objects.all()
    form = forms.PlanForm(request.POST, request.FILES,)
    if request.method == 'POST':

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect('add_Plan')
        else:
            messages.info(request, "product is not added ,try again ")
    else:
        form = forms.PlanForm()

    return render(request, 'mainadmin/add_plan.html', {'form': form, 'plan': plan, })



def updatePlan(request, id):
    
    plan = models.Creator_SubscribationPlan.objects.all()
    try:
        obj = models.Creator_SubscribationPlan.objects.get(id=id)
    except models.User.DoesNotExist:
        return HttpResponse("invalid Viseos!")

    if request.method == "POST":
        form = forms.PlanForm(
        data=request.POST, instance=obj)
        if form.is_valid():
            video=form.save(commit=False)
            if 'image' in request.FILES:
                video.image = request.FILES['image']
           
            video.save()
            return redirect('add_Plan')
        else:
            print('form error')
    else:
        plan = models.Creator_SubscribationPlan.objects.all()
        form = forms.PlanForm(instance=obj)
    
    return render(request, 'mainadmin/update_plan.html', {'form': form, 'obj': obj, 'plan': plan,  })

def deletePlan(request, id):

    obj = models.Creator_SubscribationPlan.objects.get(id=id)
    obj.delete()
    return redirect('add_Plan')

################################# IP prevent ####################################

from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver

@receiver(user_logged_in)
def remove_other_sessions(sender, user, request, **kwargs):
    # remove other sessions
    Session.objects.filter(usersession__user=user).delete()
    
    # save current session
    request.session.save()

    # create a link from the user to the current session (for later removal)
    UserSession.objects.get_or_create(
        user=user,
        session_id=request.session.session_key
    )

def creator_summary(request):
    try :
        if request.method == 'POST':
            fromdate = request.POST.get('fromdate')
            todate = request.POST.get('todate')
            searchresult = models.Subscription.objects.raw('select id,user_id,start_date,razorpay_order_id from accounts_subscription where start_date between"'+fromdate+'" and "'+todate+'"')
        
            return render(request,'mainadmin/creator_summary.html',{'rez':searchresult,'fromdate':fromdate,'todate':todate})
        else:
            rez= models.Subscription.objects.all()
            return render(request,'mainadmin/creator_summary.html',{'rez':rez})
    except:
        return redirect('rezorpaylist')


def creator_login_logout_report(request):
    video = models.CreatorAddVideo.objects.all().count()
    crt =models.Creator.objects.all()
   
    for i in crt:
        c = i.user.last_login
        d = i.last_logout
        v = d - c 
        
     
        k = i.user.username
        print(v,k)
      
        return render(request,'mainadmin/crt_login_and_upload_report.html',{'crt':crt,'v':v,'k':k})
  
def creatorblock(request,id):
    creator = User.objects.det(id=id)
    creator.is_active=False
    return redirect('listofcreator')

def creatorUnblock(request,id):
    creator = User.objects.det(id=id)
    creator.is_active=True
    return redirect('listofcreator')