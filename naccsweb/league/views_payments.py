from django.shortcuts import render, redirect
import paypalrestsdk as paypal
from paypalrestsdk import *
from django.contrib.auth.decorators import login_required
from django.conf import settings as django_settings
from django.http import HttpResponseServerError
from django.utils import timezone

import logging # Sentry

from .models import User, Player, Payment, Division

paypal.configure({
    "mode": django_settings.PAYPAL_MODE,  # sandbox or live
    "client_id": django_settings.PAYPAL_CLIENT_ID,
    "client_secret": django_settings.CLIENT_SECRET})

def needs_to_pay(player):
    """
    Returns true if player needs to pay
    """
    num_main = get_num_main_paid(Player.objects.filter(team=player.team))

    if num_main > 5:
        # Needs to pay if less than sub fee
        player.amount_paid < player.team.division.sub_fee
    else:
        # Needs to pay main fee
        return player.amount_paid < player.team.division.fee

def check_ready(team):
    # Check if has 5 main paid players
    players = Player.objects.filter(team=team)

    num_main = get_num_main_paid(players)

    if num_main >= 5: # 5 = Full roster
        team.is_ready = True
        team.save()
    else:
        team.is_ready = False
        team.save()


def get_num_main_paid(players):
    """
    Returns number of main players within input
    """
    main_fee = players[0].team.division.fee
    num_main = 0

    for p in players:
        if p.amount_paid >= main_fee:
            num_main += 1

    return num_main

def get_payment_items(players):
    """
    Input: Player names of all the same team and division
    """
    # Get all players on the same team.
    team = Player.objects.get(user__username=players[0]).team
    roster = Player.objects.filter(team=team)

    main_fee = team.division.fee
    sub_fee  = team.division.sub_fee
    
    num_main = get_num_main_paid(roster)
    items = {}

    for player in players:
        player = Player.objects.get(user__username=player)

        if num_main < 5:
            # This player should pay main fee
            items[player.user.username] = main_fee - player.amount_paid
            num_main += 1
        else:
            # This player should pay min fee
            items[player.user.username] = sub_fee - player.amount_paid

    return items

def create_itemized_payment(domain, description, items, team_id=-1):
    """
    Args:
        domain (str): Host domain
        description (str): Payment Description
        items (dict): Player name -> Amount player needs paid
    """

    payment_items = []
    
    total_amount = 0
    for name in items:
        payment_item = {
            "name": name,
            "price": items[name],
            "currency": "USD",
            "quantity": 1,
        }
        payment_items.append(payment_item)
        total_amount += items[name]
    
    if team_id == -1:
        redirect_urls = {
            "return_url": "http://" + domain + "/payment_return?success=true",
            "cancel_url": "http://" + domain + "/payment_return?cancel=true"
        }
    else:
        redirect_urls = {
            "return_url": "http://" + domain + "/payment_return?success=true&team_id=" + team_id,
            "cancel_url": "http://" + domain + "/payment_return?cancel=true&team_id=" + team_id
        }

    payment = paypal.Payment({
        "intent": "sale",

        # Payer
        # A resource representing a Payer that funds a payment
        # Payment Method as 'paypal'
        "payer": {
            "payment_method": "paypal"
        },

        # Redirect URLs
        "redirect_urls": redirect_urls,

        # Transaction
        # A transaction defines the contract of a
        # payment - what is the payment for and who
        # is fulfilling it.
        "transactions": [{

            # ItemList
            "item_list": {
                "items": payment_items
            },

            # Amount
            # Let's you specify a payment amount.
            "amount": {
                "total": total_amount,
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
