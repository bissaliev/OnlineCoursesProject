from django.contrib import admin

from .models import Balance, CustomUser, Subscription

admin.site.register(CustomUser)
admin.site.register(Balance)
admin.site.register(Subscription)
