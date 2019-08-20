from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .oauth import get_discord_name, get_faceit_name
from .schools import get_schools
from .forms import CollegeForm
from .email import email_college_confirmation, check_token

def verify(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and check_token(user, token):
        user.profile.verified_student = True
        user.save()
        return redirect('account')
    else:
        return render(request, 'verification/verification_invalid.html')

@login_required
def account(request):
    schools = get_schools()

    if request.method == 'POST':
        # Check if resend was hit
        if ('resend' in request.POST):
            user = User.objects.get(username=request.user.username)
            email_college_confirmation(user.profile.college_email, request)
            return redirect('pending')
            
        form = CollegeForm(request.POST, schools=schools)

        if form.is_valid():
            college = form.cleaned_data['college']
            email = form.cleaned_data['email']

            user = User.objects.get(username=request.user.username)
            user.profile.college_email = email
            user.profile.college = college
            user.save()

            email_college_confirmation(email, request)
            return redirect('pending')
    else:
        form = CollegeForm(schools=schools)
    

    return render(request, 'settings/account.html', {'form': form})

@login_required
def pending(request):
    print (request.user.profile.verified_student)
    if request.user.profile.verified_student:
        return redirect('/')
    return render(request, 'verification/verification_pending.html') 

@login_required
def faceit(request):
    faceit_code = request.GET.get('code')

    if (faceit_code == None):
        return redirect('account')

    faceit_username = get_faceit_name(faceit_code)

    # Enter faceit name into user profile
    user = User.objects.get(username=request.user.username)
    user.profile.faceit = faceit_username
    user.save()

    return redirect('account')
    
@login_required
def discord(request):
    discord_code = request.GET.get('code')

    if (discord_code == None):
        return redirect('account')

    discord_name = get_discord_name(discord_code)

    # Enter discord name into user profile
    user = User.objects.get(username=request.user.username)
    user.profile.discord = discord_name
    user.save()
    return redirect('account')