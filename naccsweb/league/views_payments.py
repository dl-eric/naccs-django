from django.shortcuts import render, redirect
import paypalrestsdk as paypal
from paypalrestsdk import *
from django.contrib.auth.decorators import login_required
from django.conf import settings as django_settings
from django.http import HttpResponseServerError
import logging # Sentry

from .models import User, Player, Payment

paypal.configure({
    "mode": django_settings.PAYPAL_MODE,  # sandbox or live
    "client_id": django_settings.PAYPAL_CLIENT_ID,
    "client_secret": django_settings.CLIENT_SECRET})

def check_ready(team):
    # Check if has 5 main paid players
    players = Player.objects.filter(team=team)

    num_main = get_num_main_paid(players)

    if num_main >= 2: # 5 = Full roster
        team.is_ready = True
        team.save()
    else:
        team.is_ready = False
        team.save()


def get_num_main_paid(players):
    main_fee = players[0].team.division.fee
    num_main = 0

    for p in players:
        if p.amount_paid >= main_fee:
            num_main += 1

    return num_main

def get_payment_amount(player):
    # Get all players on the same team.
    players = Player.objects.filter(team=player.team)

    main_fee = player.team.division.fee
    sub_fee  = player.team.division.sub_fee
    
    num_main = get_num_main_paid(players)

    if num_main < 5:
        # This player should pay main fee
        amount = main_fee - player.amount_paid
    else:
        # This player should pay min fee
        amount = sub_fee - player.amount_paid

    return amount


def create_payment(domain, name, price, description):
    """
    Creates a PayPal payment and returns a redirect URL on success.
    On failure, it returns None
    """

    payment=paypal.Payment({
        "intent": "sale",

        # Payer
        # A resource representing a Payer that funds a payment
        # Payment Method as 'paypal'
        "payer": {
            "payment_method": "paypal"},

        # Redirect URLs
        "redirect_urls": {
            "return_url": "http://" + domain + "/payment_return?success=true",
            "cancel_url": "http://" + domain + "/payment_return?cancel=true"
        },

        # Transaction
        # A transaction defines the contract of a
        # payment - what is the payment for and who
        # is fulfilling it.
        "transactions": [{

            # ItemList
            "item_list": {
                "items": [{
                    "name": name,
                    "sku": "fee",
                    "price": price,
                    "currency": "USD",
                    "quantity": 1}]},

            # Amount
            # Let's you specify a payment amount.
            "amount": {
                "total": price,
                "currency": "USD"},
            "description": description}]
    })

    return payment

@login_required
def pay_fee(request):
    try:
        player = Player.objects.get(user__username=request.user)
    except:
        # User is not a player, they shouldn't be here.
        redirect('account')

    # Determine how much the player has to pay
    amount = get_payment_amount(player)
    payment = create_payment(request.get_host(), player.team.division.name + " Fee", str(amount), "League fee for NACCS 2019-2020")

    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
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
        user = User.objects.get(username=request.user)
        player = Player.objects.get(user=user)

        # ID of the payment. This ID is provided when creating payment.
        paymentId = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        payment = paypal.Payment.find(paymentId)
        
        # PayerID is required to approve the payment.
        if payment.execute({"payer_id": payer_id}):
            payment = paypal.Payment.find(paymentId)
            amount_paid = payment.transactions[0].amount.total
            
            newPayment = Payment(
                name=request.user, paymentid=paymentId, payerid=payer_id, user=user, amount=amount_paid)
            newPayment.save()
            player.amount_paid += float(amount_paid)
            player.save()

            # Check if their team is ready now
            check_ready(player.team)
            return redirect('account')
        else:
            logging.error("Payment failed!", exc_info=True)
            return redirect('index')
    
    else: # Assume we're in the cancel flow
        return redirect('account')
