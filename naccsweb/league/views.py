from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from django.utils import timezone

from watson import search as watson
import logging

from .forms import SchoolSearchForm, CreateTeamForm, JoinTeamForm, EditTeamForm
from .models import School, Team, Player, Payment
from .payment_utils import check_ready, create_itemized_payment, get_payment_items, needs_to_pay

def on_a_team(user):
    '''
    Checks if <user> is already on a team
    '''

    try:
        player = Player.objects.get(user=user)
        on_team = player.team != None
    except:
        on_team = False

    return on_team


def can_join_team(user, school):
    '''
    Checks if <user> can join a team on <school>
    '''

    has_email = user.profile.college_email.endswith(school.email_domain)

    return has_email and not on_a_team(user)


def can_create_team(user, school):
    '''
    Checks if <user> can create a team at <school>
    '''

    has_email = user.profile.college_email.endswith(school.email_domain)
    is_captain = Team.objects.filter(captain=user).exists()

    return has_email and not is_captain and not on_a_team(user)


@login_required
def manage_team(request, team_id):
    if request.method == 'POST':
        players_to_pay = request.POST.getlist('pay_checkbox')

        if 'team_info' in request.POST:
            team = Team.objects.get(id=team_id)
            form = EditTeamForm(request.POST, instance=team)
            if form.is_valid():
                form.save()
        elif 'pay' in request.POST and len(players_to_pay) == 0:
            # They hit pay but nothing was checked
            pass
        elif 'pay' in request.POST:
            # They want to pay
            players_to_pay = request.POST.getlist('pay_checkbox')

            items = get_payment_items(players_to_pay)
            payment = create_itemized_payment(request.get_host(), "Bulk Pay for NACCS 2019-2020", items, team_id=team_id)
                
            if payment.create():
                print("Payment[%s] created successfully" % (payment.id))
                players = Player.objects.filter(user__username__in=players_to_pay)
                new_payment = Payment(paymentid=payment.id, payerid=None, date=timezone.now())
                new_payment.save()
                new_payment.users.set(players)
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
                logging.error("Bulk payment failed!", exc_info=True)
                print("Error while creating payment:")
                print(payment.error)
                return HttpResponseServerError()
        elif 'kick' in request.POST:
            # They want to kick a player.
            name = request.POST.get('kick')
            try:
                delete_user = User.objects.get(username=name)
                to_delete = Player.objects.get(user=delete_user)
                to_delete.team = None
                to_delete.save()
            except:
                print("Unable to delete user", name)
            redirect('manage_team', team_id)

    user = User.objects.get(username=request.user)

    try:
        team = Team.objects.get(id=team_id)

        # Check if player is on the team
        Player.objects.get(user=user, team=team)

        # Get roster of the team
        roster = Player.objects.filter(team=team).order_by('-amount_paid')

        # Check if any players need to pay
        create_payment_button = False
        for player in roster:
            if needs_to_pay(player):
                create_payment_button = True
                break

    except:
        logging.error("Getting roster", exc_info=True)
        return redirect('index')

    form = EditTeamForm(instance=team)

    return render(request, 'manage_team.html', {'create_payment_button': create_payment_button, 'form': form, 'user': user, 'team': team, 'roster': roster})


def team_pending(request):
    return render(request, 'team_pending.html')

@login_required
def create_team(request, school_id):
    # Make sure we have a valid school_id
    try:
        school = School.objects.get(id=school_id)
    except:
        return redirect('index')

    user = User.objects.get(username=request.user)

    # Redirect users that can't create teams. They shouldn't be here!
    if not can_create_team(user, school):
        return redirect('index')

    if request.method == 'POST':
        form = CreateTeamForm(request.POST, school_id=school_id)

        if form.is_valid():
            team = form.save(commit=False)
            team.captain = user
            team.school = school
            team.save()

            # Create player object if user isn't one.
            if not Player.objects.filter(user=user).exists():
                player = Player.objects.create(user=user, team=team)
            else:
                player = Player.objects.get(user=user)
                player.team = team
                player.save()

            return redirect('team_pending')
    else:
        form = CreateTeamForm(school_id=school_id)

    return render(request, 'create_team.html', {'school': school, 'form': form})


@login_required
def join_team(request, school_id):
    # Make sure we have a valid school_id
    try:
        school = School.objects.get(id=school_id)
    except:
        return redirect('index')

    user = User.objects.get(username=request.user)

    # Redirect users that can't join teams. They shouldn't be here!
    if not can_join_team(user, school):
        return redirect('index')

    teams = Team.objects.filter(school=school)

    if request.method == 'POST':
        form = JoinTeamForm(request.POST, teams=teams)

        if form.is_valid():
            # Is valid means password passes!
            team = Team.objects.get(school=school, name=form.data['teams'])
            try:
                player = Player.objects.get(user=user)
                player.team = team
                player.save()

                # Check if this player can make the team ready
                check_ready(team)
            except:
                # Player doesn't exist
                player = Player.objects.create(user=user, team=team)

            return redirect('school', school_id)
    
    else:
        form = JoinTeamForm(teams=teams)

    return render(request, 'join_team.html', {'school': school, 'form': form})


def school_search(request):
    if (request.method == "POST"):
        form = SchoolSearchForm(request.POST)

        if (form.is_valid()):
            search_results = watson.filter(School, form.data['query'])
        else:
            search_results = []
    else:
        form = SchoolSearchForm()
        search_results = School.objects.filter(is_active=True)

    return render(request, 'school/search.html', {'form': form, 'results': search_results})


def school(request, school_id):
    try:
        school = School.objects.get(id=school_id)
    except:
        return redirect('not_found')

    try:
        d1team = Team.objects.get(school=school, division__name="Division 1")
    except:
        d1team = None

    try:
        d2teams = Team.objects.filter(school=school, division__name="Division 2")
        d2 = []
        for d2team in d2teams:
            # Get roster
            d2team_roster = Player.objects.filter(team=d2team)
            d2.append((d2team, d2team_roster))
    except:
        d2 = None

    try:
        user = User.objects.get(username=request.user)
        can_create = can_create_team(user, school)
        can_join = can_join_team(user, school)

        try:
            team = Team.objects.get(school=school, captain=user)
        except:
            team = None
    except:
        # Not logged in
        can_create = False
        can_join = False
        team = None

    d1team_roster = Player.objects.filter(team=d1team)

    return render(request, 'school/school.html', {'team': team, 'can_join': can_join, 'can_create': can_create, 'school': school, 'd1team': d1team, 'd1team_roster': d1team_roster, 'd2teams': d2})


def hub(request):
    return render(request, 'hub.html')


def league(request):
    return render(request, 'league.html')