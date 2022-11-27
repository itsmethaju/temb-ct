from django.contrib import admin
from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required
urlpatterns = [



    path('',views.home,name='home'),

  
    path('privecy',views.privecy,name="privecy"),
    path('test',views.test,name="test"),
    path('creator-dash',views.crt,name='creator-dash'),

    path('plans',views.plans,name='plans'),

    path('adminclick', views.adminclick_view),
    path('doctorclick', views.createrclick_view),
    path('patientclick', views.customerclick_view),

    path('addadmins', views.admin_signup_view,name="addadmins"),
    path('creatorsignup', views.creater_signup_view,name='creatorsignup'),
    path('customersignup', views.customr_signup_view,name="customersignup"),
    path('payment',views.payment,name='payment'),

    path('adminlogin', LoginView.as_view(template_name='login.html')),
    path('creatorlogin',views.creatorlogin,name="creatorlogin"),
    path('customerlogin', views.customerlogin,name="customerlogin"),

	path('handlerequest/<int:id>',views.handlerequest,name='handlerequest'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='first-page.html'),name='logout'),

    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('add_item/<int:pk>',views.add_item,name='add_item'),
	path('checkout/<int:pk>',views.checkout,name='checkout'),

	path('pay_cancel',views.pay_cancel,name='pay_cancel'),

    path('activate_plan/<int:id>',views.activate_plan,name='activate_plan'),
    path('creator-dashboard/<str:username>',views.creator_dashboard_view,name='creator-dashboard'),
    path('videosingleview/<int:id>',views.videosingleview,name='videosingleview'),

    path('crt_addvideo',views.crt_addvideo,name='crt_addvideo'),
    path('crt_addvideolink',views.crt_addvideolink,name='crt_addvideolink'),
    path('videolist',views.videolist,name='videolist'),
    path('deleteVideo/<int:id>',views.deleteVideo,name='deleteVideo'),
    path('videoupdate/<int:id>',views.videoupdate,name='videoupdate'),

    path('videoupdatelink/<int:id>',views.videoupdatelink,name='videoupdatelink'),
    path( 'profile_view/<str:username>', views.profile, name='profile_view'),

    path('videocategory',views.videocategory,name='videocategory'),

    path('deletecaregory/<int:id>',views.deletecaregory,name='deletecaregory'),
    path('updatecategory/<int:id>',views.updatecategory,name='updatecategory'),

    path('current_plane',views.current_plane,name='current_plane'),


    path('profileview',views.profileview,name='profileview'),
    #########################################################################
    path('sub_add_item/<int:pk>',views.sub_add_item,name='sub_add_item'),
	path('sub_checkout/<int:pk>',views.sub_checkout,name='sub_checkout'),
    path('sub_payment',views.sub_payment,name='sub_payment'),
    path('sub_handlerequest',views. sub_handlerequest,name=' sub_handlerequest'),
	path('pay_cancel',views.pay_cancel,name='pay_cancel'),

    path('customer_dashboard',views.customer_dashboard,name='customer_dashboard'),
    path('customer_video_det/<int:id>',views.customer_video_det,name='customer_video_det'),
    path('subscriberlist',views.subscriberlist,name='subscriberlist'),
    path('otp' ,views.otp , name="otp"),
    path('coustomer_otp' ,views.coustomer_otp , name="coustomer_otp"),
    path('sub_wishlist_item/<int:pk>',views.sub_wishlist_item,name='sub_wishlist_item'),
    path('sub_series_wishlist_item/<int:pk>',views.sub_series_wishlist_item,name='sub_series_wishlist_item'),
    path('sub_download_video/<int:pk>',views.sub_download_video,name='sub_download_video'),
    path('download_video_detail/<int:pk>',views.download_video_detail,name='download_video_detail'),
    path('subscribers_logout',views.subscribers_logout,name='subscribers_logout'),

    ###############################################################################
    path('crt_PlalistVideo',views.crt_PlalistVideo,name='crt_PlalistVideo'),
    path('crt_PlalistVideolinkmode',views.crt_PlalistVideolinkmode,name='crt_PlalistVideolinkmode'),#link
    path('videoPlaylist',views.videoPlaylist,name='videoPlaylist'),
    path('deleteVideoLIst/<int:id>',views.deleteVideoLIst,name='deleteVideoLIst'),
    path('videoupdateList/<int:id>',views.videoupdateList,name='videoupdateList'),

    path('videoupdateListlinkt/<int:id>',views.videoupdateListlink,name='videoupdateListlink'),

    path('seriessingleview/<int:id>',views.seriessingleview,name='seriessingleview'),
    #################################################################################

    path('add_PlalistVideo',views.add_PlalistVideo,name='add_PlalistVideo'),
    path('add_PlalistVideolinkmode',views.add_PlalistVideolinkmode,name='add_PlalistVideolinkmode'),#link
    path('videoserieslist',views.videoserieslist,name='videoserieslist'),
    path('deleteVideoseries/<int:id>',views.deleteVideoseries,name='deleteVideoseries'),
    path('videoupdateseries/<int:id>',views.videoupdateseries,name='videoupdateseries'),
    path('videoupdateserieslink/<int:id>',views.videoupdateserieslink,name='videoupdateserieslink'),

    path('seriesvideosingleview/<int:id>',views.seriesvideosingleview,name='seriesvideosingleview'),
    path('cust_seriesvideosingleview/<int:id>',views.cust_seriesvideosingleview,name='cust_seriesvideosingleview'),
#========================================================================================================

    path('sub_series_add_item/<int:pk>',views.sub_series_add_item,name='sub_series_add_item'),
	path('sub_series_checkout/<int:pk>',views.sub_series_checkout,name='sub_series_checkout'),
    path('sub_series_payment',views.sub_series_payment,name='sub_series_payment'),
    path('sub_series_handlerequest',views. sub_series_handlerequest,name=' sub_series_handlerequest'),
    path('customer_series_video_det/<int:id>',views.customer_series_video_det,name='customer_series_video_det'),

#===================================================================================================================
    path('forget-password/' , views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/' , views.ChangePassword , name="change_password"),
############################################################################################
    path('Subscriber_ForgetPassword/' , views.Subscriber_ForgetPassword , name="Subscriber_ForgetPassword"),
    path('Subscriber_ChangePassword/<token>/' , views.Subscriber_ChangePassword , name="Subscriber_ChangePassword"),
#############################################################################################
    path('update_user' , views.update_user, name="update_user"),
    path('deleteWishlist/<int:id>' , views.deleteWishlist, name="deleteWishlist"),
#============================================================================================================
    path('morevideo/<int:id>' , views.morevideo , name="morevideo"),

######################## ADMIN #############################################################################
    path('dashbordadmin' , views.dashbordadmin , name="dashbordadmin"),
    path('admincreatorview/<int:id>',views.admincreatorview,name='admincreatorview'),
    path('listofcreator' , views.listofcreator , name="listofcreator"),
    path('deleteCreator/<int:id>' , views.deleteCreator, name="deleteCreator"),
    path('receipts' , views.receipts, name="receipts"),
    path('rezorpaylist' , views.rezorpaylist, name="rezorpaylist"),
#################################################################################################################



    path('adminsubscribersview/<int:id>',views.adminsubscribersview,name='adminsubscribersview'),
    path('deletesubscribers/<int:id>' , views.deletesubscribers, name="deletesubscribers"),

    path('listofsubscribers' , views.listofsubscribers , name="listofsubscribers"),
    path('subreceipts' , views.subreceipts, name="subreceipts"),
    path('subrezorpaylist' , views.subrezorpaylist, name="subrezorpaylist"),
#########################################################################################################################

    path('admin_addvideo',views.admin_addvideo,name='admin_addvideo'),
    path('admin_addvideolink',views.admin_addvideolink,name='admin_addvideolink'),

    path('admin_videolist',views.admin_videolist,name='admin_videolist'),
    path('admin_deleteVideo/<int:id>',views.admin_deleteVideo,name='admin_deleteVideo'),
    path('admin_videoupdate/<int:id>',views.admin_videoupdate,name='admin_videoupdate'),
    path('allVideolist',views.allVideolist,name='allVideolist'),

    path('admin_SeriesVideo',views. admin_SeriesVideo,name= 'admin_SeriesVideo'),
    path('admin_serieslinkmode',views.admin_serieslinkmode,name='admin_serieslinkmode'),

    path('admin_PlalistVideo',views. admin_PlalistVideo,name= 'admin_PlalistVideo'),
    path('admin_PlalistVideolinkmode',views.admin_PlalistVideolinkmode,name='admin_PlalistVideolinkmode'),
    path('see_users',views.see_users,name='see_users'),

########################################################################################################################
    path('addadmins', views.admin_signup_view,name="addadmins"),
    path('adminslist', views.adminslist,name="adminslist"),
    path('deleteadmin/<int:id>', views.deleteadmin,name="deleteadmin"),

    path('adminvideocategory',views.adminvideocategory,name='adminvideocategory'),
    path('admincaregory_list',views.admincaregory_list,name='admincaregory_list'),
    path('admindeletecaregory/<int:id>',views.admindeletecaregory,name='admindeletecaregory'),
    path('adminupdatecategory/<int:id>',views.adminupdatecategory,name='adminupdatecategory'),


    path('add_Plan',views.add_Plan,name='add_Plan'),
    path('updatePlan/<int:id>',views.updatePlan,name='updatePlan'),
    path('deletePlan/<int:id>', views.deletePlan,name="deletePlan"),


###################################################################################
    path('creator_summary',views.creator_summary,name='creator_summary'),
    path('creator_login_logout_report',views.creator_login_logout_report,name="creator_login_logout_report"),


############################################################################
    path('creatorblock/<int:id>', views.creatorblock,name="creatorblock"),
    path('creatorUnblock/<int:id>', views.creatorUnblock,name="creatorUnblock"),
]
