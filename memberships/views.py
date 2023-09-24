from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from .models import Membership, UserMembership, Subscription, UserProfile
from .forms import UserProfileUpdateForm
import json
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY



def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None

def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(user_membership = get_user_membership(request))
    if user_subscription_qs.exists():
        return user_subscription_qs.first()
    return None

def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(membership_type=membership_type)

    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'memberships/user_profile_detail.html'  # Create this template in your templates folder
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['user_membership'] = UserMembership.objects.get(user=self.request.user)
        return context

    def get_object(self):
        username = self.kwargs.get("username")
        return get_object_or_404(UserProfile, user__username=username)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateForm
    template_name = 'memberships/user_profile_update.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        user = get_object_or_404(User, username=username)
        return get_object_or_404(UserProfile, user=user)



class MembershipSelectView(ListView):
    model = Membership

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self,request, *args, **kwargs):
        selected_membership_type = request.POST.get('membership_type')

        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        selected_membership_qs = Membership.objects.filter(membership_type=selected_membership_type)

        if selected_membership_qs.exists():
            selected_membership= selected_membership_qs.first()

        # Validation

        if user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(request, 'You already have this membership. Your next payment is due {}'.format('get this value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # assign to the Sessions
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('memberships:payment'))



def PaymentView(request):

    user_membership = get_user_membership(request)

    selected_membership = get_selected_membership(request)

    publishkey = settings.STRIPE_PUBLISABLE_KEY

    context = {
        'publishkey': publishkey,
        'selected_membership': selected_membership
    }

    return render(request, 'memberships/membership_payment.html', context)



def handle_payment(request):
    if request.method == 'POST':

        # Retrieve selected subscription tier from form data
        selected_membership = get_selected_membership(request)

        # Map selected tier to Stripe Price ID
        stripe_price_ids = {
            'Free': 'price_1NrGwDIIrFwTHqtymrm368Ml',
            'Professional': 'price_1NrGwDIIrFwTHqtyjbljyRwZ',
            'Enterprise': 'price_1NrGwDIIrFwTHqtyVYz2iL4p',
        }

        stripe_price_id = stripe_price_ids.get(selected_membership)

        if not stripe_price_id:
            return JsonResponse({'status': 'error', 'message': 'Invalid subscription tier'})

        # The payment token sent by Stripe.js (this would actually come from your frontend)
        payment_token = request.POST.get('stripeToken')

        # Your user (this would be fetched from the request in a real-world scenario)
        user = request.user
        user_email = user.email  # Replace with the user's email



        try:
            # Step 1: Create Stripe Customer
            customer = stripe.Customer.create(
                email=user_email,
                source=payment_token  # obtained with Stripe.js
            )

            

            # Step 3: Create Subscription
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        'price': 'your_price_id',  # Use the Stripe Price ID mapped from the selected tier
                    },
                ]
            )

            # Update UserMembership
            user_membership = get_user_membership(request)

            user_membership.stripe_customer_id = customer.id
            user_membership.save()

            # Update or Create Subscription
            subscription_record, created = Subscription.objects.get_or_create(
                user_membership=user_membership
            )

            subscription_record.stripe_subscription_id = subscription.id
            subscription_record.active = True
            subscription_record.save()


            return JsonResponse({'status': 'success'})

        except stripe.error.StripeError as e:
            # Handle Stripe-specific exceptions
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'status': 'failure', 'error': str(e)})

    # Handle the event
    if event.type == 'invoice.paid':
        # Payment was successful
        # Update user subscription state
        pass

    elif event.type == 'invoice.payment_failed':
        # Payment failed
        # Update user subscription state
        pass

    # ... handle other event types

    return JsonResponse({'status': 'success'})
