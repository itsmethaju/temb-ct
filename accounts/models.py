from email.mime import image
from pyclbr import Class
from unicodedata import category
from urllib import request
from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import date, timedelta
from datetime import datetime as dt
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
today = datetime.date.today()
from django.db.models.signals import post_save
from django.urls import reverse
from django.db.models.signals import post_delete
from embed_video.fields import EmbedVideoField
from django.dispatch import receiver
from indian_cities.dj_city import cities
from PIL import Image
today = datetime.date.today()
from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
from django.conf import settings
# As model field:
from django_currentuser.db.models import CurrentUserField
from django.contrib.sessions.models import Session


Gender=[('Male','Male'),
('FeMale','Female'),
('Other','Other'),
]
Plane =[('OneMonth','OneMonth'),
('OneYear','Oneyear')
]
state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))


class Admins(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE )
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    last_logout = models.DateTimeField(blank=True, null=True)


class Creator(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE ,primary_key=True)
    profile= models.ImageField(upload_to='Creatorprofile',null=True,)
    address = models.TextField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    gender= models.CharField(max_length=50,choices=Gender,default='Male')
    email =models.CharField(max_length=40)
    coverphoto= models.ImageField(upload_to='Creatorprofile',null=True,blank=True)
    city = models.CharField(choices=cities, null=False, max_length=20)
    state = models.CharField(choices=state_choices,max_length=255, null=True, blank=True)
    bankname= models.CharField(max_length=50,null=True,blank=True)
    branch = models.CharField(max_length=150,null=True,blank=True)
    accountholdername= models.CharField(max_length=250,null=True,blank=True)
    accountnumber = models.IntegerField(null=True,blank=True)
    ifc=models.CharField(max_length=100,null=True,blank=True)
    status=models.BooleanField(default=False)
    otp = models.CharField(max_length=6)
    date = models.DateTimeField(blank=True, null=True)
    last_logout = models.DateTimeField(blank=True, null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.gender)




class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    mobile = models.CharField(max_length=20,null=False)
    otp = models.CharField(max_length=6)
    email =models.CharField(max_length=40)
    status=models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add = True)
    last_logout = models.DateTimeField(blank=True, null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name
Plane_type=[('Reelcat Exhibit','Reelcat Exhibit'),
('Reelcat Basic','Reelcat Basic'),
('Reelcat Premium','Reelcat Premium'),
]
Plane_periods=[('1 year','365'),
('1week','7'),
('One month','30',),
]
duration=[(365,365),
(7,7),
(30,30,),
]
class Creator_SubscribationPlan(models.Model):
    image = models.ImageField(upload_to='subplan',null=True,)
    plan_type = models.CharField(max_length=50,choices=Plane_type,default='Standard')
    plane_period =models.CharField(max_length=50,choices=Plane_periods,default='One month')
    duration = models.PositiveIntegerField(choices=duration,default=7)
    Gst = models.IntegerField()
    plane_price =models.IntegerField()
    plane_desc1 = models.CharField(max_length=100)
    plane_desc2 = models.CharField(max_length=100)
    plane_desc3 = models.CharField(max_length=100)
    plane_desc4 = models.CharField(max_length=100)
    plane_desc5 = models.CharField(max_length=100)
    plane_desc6 = models.CharField(max_length=100)

    def __str__(self):
        return self.plan_type
    def get_add_to_cart_url(self):
        return reverse('add_to_cart',kwargs ={
            'pk':self.pk
        })



# Subscriber
class Subscriber(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	mobile=models.CharField(max_length=20)
	img=models.ImageField(upload_to="subs/",null=True)

	def __str__(self):
		return str(self.user)



@receiver(post_save,sender=User)
def create_subscriber(sender,instance,created,**kwrags):
	if created:
		Subscriber.objects.create(user=instance)

# Subscription
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default = False)
    expires_in = models.DateField(null=True, blank=True)
    product = models.ForeignKey(Creator_SubscribationPlan, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
    class Meta:
        db_table="OrderItem"
        
    def __str__(self):
        return  self.product.plan_type

    def get_total_item_price(self):
        return  self.product.plane_price + self.product.Gst

    def get_final_price(self):
        return self.product.plane_price

@receiver(post_save, sender=OrderItem,)
def update_active(sender, instance, created, **kwargs):
	if instance.expires_in < today:

		subscription =  OrderItem.objects.get(id=instance.id)

		subscription.delete()







class Subscription(models.Model):
    user= models.ForeignKey(User, on_delete = models.CASCADE)

    items = models.ManyToManyField(OrderItem)

    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add = True)
    ordered = models.BooleanField(default =False)
    ordered_id = models.CharField(max_length = 100,unique=True,default = None,blank =True,null = True)
    date_of_payment = models.DateTimeField(auto_now_add = True)

    # checkout_address=models.ForeignKey(CheckoutAddress,on_delete = models.CASCADE)
    razorpay_order_id = models.CharField(max_length =500,null=True,blank = True)
    razorpay_payment_id = models.CharField(max_length =500,null=True,blank =True)
    razorpay_signature = models.CharField(max_length=500,null=True,blank =True)
    razorpay_expanse = models.PositiveIntegerField(default=6)


    def save(self,*args,**kwargs):
        if self.ordered_id is None and self.date_of_payment and self.id:
            self.ordered_id = self.date_of_payment.strftime('PAY2ME%y%m%d0DR')+str(self.id)

        return super().save(*args,**kwargs)

    def __str__(self):
        return self.user.username
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total = order_item.get_total_item_price()
        return total


class VideoCaregory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    titel = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
         return self.titel

    @property
    def get_products(self):
        return CreatorAddVideo.objects.filter(category__titel=self.titel)


class CreatorAddVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    category = models.ForeignKey(VideoCaregory, on_delete=models.CASCADE)
    videofile =models.FileField(upload_to='Creatorvideo',null=True,)
    videolink = EmbedVideoField()
    titel = models.CharField(max_length=250)
    image = models.ImageField(upload_to='Creatorvideo',null=True,)
    language = models.CharField(max_length=250)
    runTime=models.CharField(max_length=250)
    price = models.IntegerField()
    desc =models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_downloaded = models.BooleanField('is_downloaded',default=False)
    def __str__(self):
         return self.titel

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width >200:
            output_size =(300,200)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Coverphoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    image = models.ImageField(upload_to='Creatrcoverphoto',null=True, blank=True)
    is_add  = models.BooleanField(default =True)

########################################################################################

class SubOrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default = False)
    product = models.ForeignKey(CreatorAddVideo, on_delete = models.CASCADE)
    date =models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return  self.product.user.username

    def get_total_item_price(self):
        return  self.product.price

    def get_final_price(self):
        return self.get_total_item_price()

class DownloadVideo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default='')
    video = models.ForeignKey(SubOrderItem, on_delete = models.CASCADE)


class SubSubscription(models.Model):
    user= models.ForeignKey(User, on_delete = models.CASCADE)

   

    items = models.ManyToManyField(SubOrderItem)

    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add = True)
    ordered = models.BooleanField(default =False)
    ordered_id = models.CharField(max_length = 100,unique=True,default = None,blank =True,null = True)
    date_of_payment = models.DateTimeField(auto_now_add = True)
############################################################################
    razorpay_order_id = models.CharField(max_length =500,null=True,blank = True)
    razorpay_payment_id = models.CharField(max_length =500,null=True,blank =True)
    razorpay_signature = models.CharField(max_length=500,null=True,blank =True)


    def save(self,*args,**kwargs):
        if self.ordered_id is None and self.date_of_payment and self.id:
            self.ordered_id = self.date_of_payment.strftime('PAY2ME%y%m%d0DR')+str(self.id)

        return super().save(*args,**kwargs)

    def __str__(self):
        return self.user.username
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total = order_item.get_final_price()
        return total

####################################
class ViewUser(models.Model):
    user =models.TextField(default=None)

    def __str__(self) :
        return self.user

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    product = models.ForeignKey(CreatorAddVideo, on_delete = models.CASCADE)



    def __str__(self):
        return  self.product.user.username


######################################################################################

class PlayLists(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default='')

    videofile =models.FileField(upload_to='Creatorplaylistvideo',null=True,)
    videolink = EmbedVideoField()
    titel = models.CharField(max_length=250)
    image = models.ImageField(upload_to='Creatorplaylistimg',null=True,)
    language = models.CharField(max_length=250)
    runTime=models.CharField(max_length=250)
    price = models.IntegerField()
    desc =models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return self.titel

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    playlists = models.ForeignKey(PlayLists, on_delete=models.CASCADE)
    videofile =models.FileField(upload_to='Creatorplaylistvideo',null=True,)
    videolink = EmbedVideoField()
    titel = models.CharField(max_length=250)
    image = models.ImageField(upload_to='Creatorplaylistimg',null=True,)
    language = models.CharField(max_length=250)
    runTime=models.CharField(max_length=250)
    desc =models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return self.titel


##################################################################################################

class SubseriesOrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default = False)
    product = models.ForeignKey(PlayLists, on_delete = models.CASCADE)
   
    def __str__(self):
        return  self.product.user.username

    def get_total_item_price(self):
        return  self.product.price

    def get_final_price(self):
        return self.get_total_item_price()

class SubseriesSubscription(models.Model):
    user= models.ForeignKey(User, on_delete = models.CASCADE)

    items = models.ManyToManyField(SubseriesOrderItem)

    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add = True)
    ordered = models.BooleanField(default =False)
    ordered_id = models.CharField(max_length = 100,unique=True,default = None,blank =True,null = True)
    date_of_payment = models.DateTimeField(auto_now_add = True)
############################################################################
    razorpay_order_id = models.CharField(max_length =500,null=True,blank = True)
    razorpay_payment_id = models.CharField(max_length =500,null=True,blank =True)
    razorpay_signature = models.CharField(max_length=500,null=True,blank =True)


    def save(self,*args,**kwargs):
        if self.ordered_id is None and self.date_of_payment and self.id:
            self.ordered_id = self.date_of_payment.strftime('PAY2ME%y%m%d0DR')+str(self.id)

        return super().save(*args,**kwargs)

    def __str__(self):
        return self.user.username
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


#####################################################################
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


#######################################################################################

from django.conf import settings
from django.db import models
from django.contrib.sessions.models import Session

class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)