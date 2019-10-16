from django.shortcuts import render, redirect
import paypalrestsdk as paypal
from paypalrestsdk import *
import os


paypal.configure({
    "mode": os.environ.get('PAYPAL_MODE'),  # sandbox or live
    "client_id": os.environ.get('SANDBOX_CLIENT_ID'),
    "client_secret": os.environ.get('SANDBOX_SECRET_ID')})



def div_one_payment():
 
    payment = paypal.Payment({
        "intent": "sale",

        # Payer
        # A resource representing a Payer that funds a payment
        # Payment Method as 'paypal'
        "payer": {
            "payment_method": "paypal"},

        # Redirect URLs
        "redirect_urls": {
            "return_url": "http://collegiatecounterstrike.com/payment_return?success=true",
            "cancel_url": "http://collegiatecounterstrike.com/payment_return?cancel=true"},

        # Transaction
        # A transaction defines the contract of a
        # payment - what is the payment for and who
        # is fulfilling it.
        "transactions": [{

            # ItemList
            "item_list": {
                "items": [{
                    "name": "Division 1 Fees",
                    "sku": "fee",
                    "price": "25.00",
                    "currency": "USD",
                    "quantity": 1}]},

            # Amount
            # Let's you specify a payment amount.
            "amount": {
                "total": "25.00",
                "currency": "USD"},
            "description": "Summer League Fees"}]})

    # Create Payment and return status
    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                # Convert to str to avoid google appengine unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                redirect_url = str(link.href)
                print("Redirect for approval: %s" % (redirect_url))
                return redirect('one_payment')
    else:
        print("Error while creating payment:")
        print(payment.error)
        return "Error while creating payment"

def div_two_payment():
    payment = paypal.Payment({
            "intent": "sale",

            # Payer
            # A resource representing a Payer that funds a payment
            # Payment Method as 'paypal'
            "payer": {
                "payment_method": "paypal"},

            # Redirect URLs
            "redirect_urls": {
                "return_url": "http://collegiatecounterstrike.com/payment_return?success=true",
                "cancel_url": "http://collegiatecounterstrike.com/payment_return?cancel=true"},

            # Transaction
            # A transaction defines the contract of a
            # payment - what is the payment for and who
            # is fulfilling it.
            "transactions": [{

                # ItemList
                "item_list": {
                    "items": [{
                        "name": "NACCS Division 2 Fees",
                        "sku": "fee",
                        "price": "10.00",
                        "currency": "USD",
                        "quantity": 1}]},

                # Amount
                # Let's you specify a payment amount.
                "amount": {
                    "total": "10.00",
                    "currency": "USD"},
                "description": "NACCS Division 2 Fees"}]})

        # Create Payment and return status
    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
            # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                    # Convert to str to avoid google appengine unicode issue
                    # https://github.com/paypal/rest-api-sdk-python/pull/58
                redirect_url = str(link.href)
                print("Redirect for approval: %s" % (redirect_url))
                return redirect('index')
    else:
        print("Error while creating payment:")
        print(payment.error)
        return "Error while creating payment"

def div_one_sub_payment():
    payment = paypal.Payment({
            "intent": "sale",

            # Payer
            # A resource representing a Payer that funds a payment
            # Payment Method as 'paypal'
            "payer": {
                "payment_method": "paypal"},

            # Redirect URLs
            "redirect_urls": {
                "return_url": "http://collegiatecounterstrike.com/payment_return?success=true",
                "cancel_url": "http://collegiatecounterstrike.com/payment_return?cancel=true"},

            # Transaction
            # A transaction defines the contract of a
            # payment - what is the payment for and who
            # is fulfilling it.
            "transactions": [{

                # ItemList
                "item_list": {
                    "items": [{
                        "name": "NACCS Division 1 Sub Fees",
                        "sku": "fee",
                        "price": "12.50",
                        "currency": "USD",
                        "quantity": 1}]},

                # Amount
                # Let's you specify a payment amount.
                "amount": {
                    "total": "12.50",
                    "currency": "USD"},
                "description": "NACCS Division 1 Sub Fees"}]})

        # Create Payment and return status
    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
            # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                    # Convert to str to avoid google appengine unicode issue
                    # https://github.com/paypal/rest-api-sdk-python/pull/58
                redirect_url = str(link.href)
                print("Redirect for approval: %s" % (redirect_url))
                return redirect('index')
    else:
        print("Error while creating payment:")
        print(payment.error)
        return "Error while creating payment"

def div_two_sub_payment():
    payment = paypal.Payment({
            "intent": "sale",

            # Payer
            # A resource representing a Payer that funds a payment
            # Payment Method as 'paypal'
            "payer": {
                "payment_method": "paypal"},

            # Redirect URLs
            "redirect_urls": {
                "return_url": "http://collegiatecounterstrike.com/payment_return?success=true",
                "cancel_url": "http://collegiatecounterstrike.com/payment_return?cancel=true"},

            # Transaction
            # A transaction defines the contract of a
            # payment - what is the payment for and who
            # is fulfilling it.
            "transactions": [{

                # ItemList
                "item_list": {
                    "items": [{
                        "name": "NACCS Division 2 Sub Fees",
                        "sku": "fee",
                        "price": "5.00",
                        "currency": "USD",
                        "quantity": 1}]},

                # Amount
                # Let's you specify a payment amount.
                "amount": {
                    "total": "5.00",
                    "currency": "USD"},
                "description": "NACCS Division 2 Sub Fees"}]})

        # Create Payment and return status
    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
            # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                    # Convert to str to avoid google appengine unicode issue
                    # https://github.com/paypal/rest-api-sdk-python/pull/58
                redirect_url = str(link.href)
                print("Redirect for approval: %s" % (redirect_url))
                return redirect('index')
    else:
        print("Error while creating payment:")
        print(payment.error)
        return "Error while creating payment"