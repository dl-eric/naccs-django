import paypalrestsdk as paypal

from .models import User, Player, Payment, Division

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