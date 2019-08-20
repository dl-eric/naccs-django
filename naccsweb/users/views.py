from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from .forms import RegisterForm, LoginForm
from .tokens import account_activation_token

# User profile view
def profile(request, page_alias):
    try:
        user = User.objects.get(username=page_alias)
    except:
        return redirect('/notfound')

    profile = {'username': user.username, 'email': user.email}
    return render(request, 'users/profile.html', context=profile)

# Register view
def register(request):
    
    def email_confirmation(user, request):
        current_site = get_current_site(request)
        subject = "Activate your NACCS account!"
        message = render_to_string('registration/account_activation_email.txt', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        html_message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
        })
        print ("Emailing user...")
        user.email_user(subject=subject, message=message, html_message=html_message)
        print ("Emailed user!")


    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            email_confirmation(user, request)
            
            return redirect('pending')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'registration/account_activation_invalid.html')

def pending(request):
    if request.user.is_active:
        return redirect('/')
    return render(request, 'registration/account_activation_pending.html') 

def not_found(request):
    return render(request, 'users/unknown.html')