from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        username = request.user.username
        url = reverse('memberships:profile', kwargs={'username': username})
        return url

    def get_signup_redirect_url(self, request, user=None):
        username = request.POST.get('username')
        url = reverse('memberships:profile', kwargs={'username': username})
        return url
