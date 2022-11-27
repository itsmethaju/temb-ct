
from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from . import models

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.fields.files import ImageFieldFile, FileField

#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }



class CreaterUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class ProfileForm(forms.ModelForm):
    class Meta:
        model=models.Creator
        fields=['profile']



class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class CustomerForm(forms.ModelForm):


    class Meta:
        model=models.Customer
        fields=['mobile','status']

class VideoForm(forms.ModelForm):

    class Meta:
        model = models.CreatorAddVideo
        exclude = ('user', 'recurring',)
        fields = fields=['titel','desc','image','videofile','category','language','runTime','price','is_downloaded']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = models.VideoCaregory.objects.filter(user=user)


class VideoLinkForm(forms.ModelForm):
    class Meta:
        model = models.CreatorAddVideo
        fields = fields=['titel','desc','image','videolink','category','language','runTime','price']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(VideoLinkForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = models.VideoCaregory.objects.filter(user=user)


class VideoCaregoryForm(forms.ModelForm):
    class Meta:
        model = models.VideoCaregory
        fields = fields=['titel']

class CaregorycoverphotoForm(forms.ModelForm):
    class Meta:
        model = models.Coverphoto
        fields = fields=['image']

class PlayListsForm(forms.ModelForm):
    class Meta:
        model = models.PlayLists
        fields = fields=['titel','desc','image','videofile','language','runTime','price']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PlayListsForm, self).__init__(*args, **kwargs)
       
class PlayListlinksForm(forms.ModelForm):
    class Meta:
        model = models.PlayLists
        fields = fields=['titel','desc','image','videolink','language','runTime','price']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PlayListlinksForm, self).__init__(*args, **kwargs)
        

class PlayListsvideoForm(forms.ModelForm):
    class Meta:
        model = models.Video
        fields = fields=['titel','desc','image','videofile','playlists','language','runTime',]
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PlayListsvideoForm, self).__init__(*args, **kwargs)
        self.fields['playlists'].queryset = models.PlayLists.objects.filter(user=user)

class PlayListsvideolinkForm(forms.ModelForm):
    class Meta:
        model = models.Video
        fields = fields=['titel','desc','image','videolink','playlists','language','runTime']
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PlayListsvideolinkForm, self).__init__(*args, **kwargs)
        self.fields['playlists'].queryset = models.PlayLists.objects.filter(user=user)


# profile update


class UserForm2(forms.ModelForm):

    class Meta:
        model = User
        fields = ( 'first_name', 'last_name','username','email',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.Creator
        fields = ('profile', 'address','gender','coverphoto','city','state','mobile','bankname','branch','accountholdername','accountnumber','ifc')






class PlanForm(forms.ModelForm):

    class Meta:
        model = models.Creator_SubscribationPlan
        
        fields = fields=['image','plan_type','plane_period','duration','Gst','plane_price','plane_desc1','plane_desc2','plane_desc3','plane_desc4','plane_desc5','plane_desc6']
    def __init__(self, *args, **kwargs):
        
        super(PlanForm, self).__init__(*args, **kwargs)
      








# Accounts
#  Coverphotos
#  Creator add videos
#  Creator_ subscribation plans
#  Creators
#  Customers
#  Order items
#  Play listss
#  Sub order items
#  Sub subscriptions
#  Subscribers
#  Subscriptions
#  Video caregorys
#  Videos
#  Wishlists
# Authentication and Authorization
#  Groups
#  Users

# class Coverphotos(forms.ModelForm):
#     class Meta:
#         model= models.Coverphoto
#         fields =(' user','image','is_add')

# class Creatoraddvideos(forms.ModelForm):
#     class Meta:
#         model =models.CreatorAddVideo
#         fields = fields=['user','titel','desc','image','videofile','category','language','runTime','price']

#  class Creator_subscribationplans(forms.ModelForm):
    #  class Meta:
    #      model= models.Coverphoto
    #      fields =('image','plan_type','plane_period','plane_price','plane_desc1','plane_desc2','plane_desc3','plane_desc4','plane_desc5','plane_desc6')

# class Coverphotos(forms.ModelForm):
#     class Meta:
#         model= models.User
#         fields =(' user','image','is_add')
