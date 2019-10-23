from django.shortcuts import render, redirect
import paypalrestsdk as paypal
from django.contrib.auth.decorators import login_required
from django.conf import settings as django_settings
from django.http import HttpResponseServerError
from django.utils import timezone

import logging # Sentry

from .payment_utils import get_payment_items, create_itemized_payment, check_ready
from .models import User, Player, Payment, Division

paypal.configure({
    "mode": django_settings.PAYPAL_MODE,  # sandbox or live
    "client_id": django_settings.PAYPAL_CLIENT_ID,
    "client_secret": django_settings.CLIENT_SECRET})


@login_required
def pay_fee(request):
    try:
        player = Player.objects.get(user__username=request.user)
    except:
        # User is not a player, they shouldn't be here.
        redirect('account')

    # Determine how much the player has to pay
    items = get_payment_items([player.user.username])
    payment = create_itemized_payment(request.get_host(), "League fee for NACCS 2019-2020", items)

    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
        new_payment = Payment(paymentid=payment.id, payerid=None, date=timezone.now())
        new_payment.save()
        new_payment.users.set([player])
        new_payment.save()
        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                # Convert to str to avoid google appengine unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                redirect_url=str(link.href)
                print("Redirect for approval: %s" % (redirect_url))
                return redirect(redirect_url)

    else:
        print("Error while creating payment:")
        print(payment.error)
        return HttpResponseServerError()

@login_required
def payment_return(request):
    # Check for success
    if request.GET.get('success') == "true":
        # ID of the payment. This ID is provided when creating payment.
        paymentId = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        payment = paypal.Payment.find(paymentId)
        
        # PayerID is required to approve the payment.
        if payment.execute({"payer_id": payer_id}):
            the_payment = Payment.objects.get(paymentid=paymentId)
            the_payment.payerid = payer_id
            the_payment.save()

            for item in payment.transactions[0].item_list.items:
                player = Player.objects.get(user__username=item.name)
                player.amount_paid += float(item.price)
                player.save()

            # Check if their team is ready now
            check_ready(player.team)
            if request.GET.get('team_id'):
                return redirect('manage_team', request.GET.get('team_id'))
            else:
                return redirect('account')
        else:
            logging.error("Payment failed!", exc_info=True)
            return redirect('index')
    
    else: # Assume we're in the cancel flow
        if request.GET.get('team_id'):
            return redirect('manage_team', request.GET.get('team_id'))
        else:
            return redirect('account')
