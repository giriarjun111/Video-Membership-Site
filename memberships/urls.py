from django.urls import path
from .views import UserProfileDetailView, UserProfileUpdateView, MembershipSelectView, PaymentView, stripe_webhook


app_name =  'memberships'

urlpatterns = [
	path('select/', MembershipSelectView.as_view(), name='select'),
	path('profile/<username>/', UserProfileDetailView.as_view(), name='profile'),
	path('profile/<username>/update/', UserProfileUpdateView.as_view(), name='profile_update'),
	path('payment/', PaymentView, name='payment'),
    path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),

]
