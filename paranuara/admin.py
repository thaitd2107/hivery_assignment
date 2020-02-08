from django.contrib import admin
from paranuara.models import Friend


class FriendAdmin(admin.ModelAdmin):
    list_display = ("people_index", "friend_index")


# Register your models here.
admin.site.register(Friend, FriendAdmin)
