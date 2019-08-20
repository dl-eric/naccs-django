from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

from django.contrib.auth.tokens import default_token_generator

def email_college_confirmation(email, request):
        token = default_token_generator.make_token(request.user)

        current_site = get_current_site(request)
        subject = "Verify your College Credentials!"
        
        html_message = render_to_string('verification/verification_email.html', {
                'user': request.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                'token': default_token_generator.make_token(request.user),
        })
        print ("Emailing user...")
        send_mail(subject, html_message, 'noreply@collegiatecounterstrike.com', [email])
        print ("Emailed user!")
        
def check_token(user, token):
    return default_token_generator.check_token(user, token)