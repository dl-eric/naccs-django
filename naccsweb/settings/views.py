from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import requests
import base64

def account(request):
    return render(request, 'settings/account.html')

def faceit(request):
    # grab faceit code from URL
    faceit_code = request.GET.get('code')
    print(faceit_code)
    # create authorization
    authorization = b'4c53be11-4f4a-4f71-845a-7a094004f4a0:T6pKFm8vR28qUWyOpe2IdIoksbs3RC5Z2DXuEM4e'
    authorization_enc = base64.b64encode(authorization)
    print(authorization_enc.decode())
    # exchange code for authorization token
    response = requests.post('https://api.faceit.com/auth/v1/oauth/token', headers={
        'Authorization': 'Basic ' + authorization_enc.decode()
    },
    data={
        'code': faceit_code,
        'grant_type': 'authorization_code'
    })

    print(response.json())

    access_token = response.json().get('access_token')
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response =  requests.get('https://api.faceit.com/auth/v1/resources/userinfo', headers=headers)
    faceit_username = response.json().get('nickname')

    user = User.objects.get(username=request.user.username)
    user.profile.faceit = faceit_username
    user.save()
    
    return redirect('account')