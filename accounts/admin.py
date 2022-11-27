from django.contrib import admin
from accounts.models import*
# Register your models here.


class CreatorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Creator, CreatorAdmin)

class SubascriberAdmin(admin.ModelAdmin):
    pass
admin.site.register(Customer, SubascriberAdmin)

class SubscriberAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subscriber, SubscriberAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrderItem, OrderItemAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Subscription, SubscriptionAdmin)

class VideoCaregoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(VideoCaregory, VideoCaregoryAdmin)

class CreatorAddVideoAdmin(admin.ModelAdmin):
    pass
admin.site.register(CreatorAddVideo, CreatorAddVideoAdmin)

class CoverphotoAdmin(admin.ModelAdmin):
    pass
admin.site.register( Coverphoto,  CoverphotoAdmin)

class SubOrderItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(SubOrderItem, SubOrderItemAdmin)
class SubSubscriptionAdmin(admin.ModelAdmin):
    pass
admin.site.register(SubSubscription, SubSubscriptionAdmin)
class Creator_SubscribationPlanAdmin(admin.ModelAdmin):
    pass
admin.site.register(Creator_SubscribationPlan, Creator_SubscribationPlanAdmin)

class WishlistAdmin(admin.ModelAdmin):
    pass
admin.site.register(Wishlist, WishlistAdmin)

class PlayListsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PlayLists, PlayListsAdmin)

class VideoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Video, VideoAdmin)
