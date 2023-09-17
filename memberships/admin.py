from django.contrib import admin
from .models import Membership, UserMembership, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ['user_membership', 'stripe_subscription_id', 'active']


@admin.register(Membership)
class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ['membership_type', 'stripe_plan_id', 'price']

@admin.register(UserMembership)
class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ['user', 'membership']
	list_filter = ['membership']
