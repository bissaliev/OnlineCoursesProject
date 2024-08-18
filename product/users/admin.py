from django.contrib import admin

from .models import Balance, CustomUser, Subscription


class BalanceInline(admin.TabularInline):
    model = Balance


class SubscriptionInline(admin.TabularInline):
    model = Subscription


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email"]
    inlines = [BalanceInline, SubscriptionInline]


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ["student", "bonus"]
    list_editable = ["bonus"]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ["course", "student"]
