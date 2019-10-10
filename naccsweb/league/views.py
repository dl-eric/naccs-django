from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import paypalrestsdk as paypal
from paypalrestsdk import *
from django.contrib.auth.decorators import login_required
from .payments import div_one_payment, div_two_payment,div_one_sub_payment,div_two_sub_payment
from .models import Payment
from .faceit import get_hub_leaderboard


from watson import search as watson

from .forms import SchoolSearchForm, CreateTeamForm, JoinTeamForm, EditTeamForm
from .models import School, Team, Player

def on_a_team(user):
    '''
    Checks if <user> is already on a team
    '''

    try:
        player = Player.objects.get(user=user)
        on_team = player.team != None
        print("on team", on_team)
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
    user = User.objects.get(username=request.user)

    try:
        team = Team.objects.get(id=team_id)

        
        # Check if player is on the team
        player = Player.objects.get(user=user, team=team)

        # Get roster of the team
        roster = Player.objects.filter(team=team)
        print(roster)

        #Get paid members of the roster
        paid_members = Player.objects.filter(team=team, has_paid = 1)
        print(paid_members)
        
    except:
        print('error')
        return redirect('index')

    form = EditTeamForm(instance=team)

    return render(request, 'manage_team.html', {'form': form, 'user': user, 'team': team, 'roster': roster, 'paid_members':paid_members})

def team_pending(request):
    return render(request, 'team_pending.html')

@login_required
def team_settings(request):
    user = User.objects.get(username=request.user)

    try:
        player = Player.objects.get(user=user)
        if player.team == None:
            redirect('index')
    except:
        redirect('index')

    team = player.team
    is_captain = team.captain == user

    return render(request, 'team.html')

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
            except:
                # Player doesn't exist
                player = Player.objects.create(user=user, team=team)

            return redirect('team_settings')
    
    else:
        form = JoinTeamForm(teams=teams)

    return render(request, 'join_team.html', {'school': school, 'form': form})

def school_search(request):
    if (request.method == "POST"):
        form = SchoolSearchForm(request.POST)

        if (form.is_valid()):
            search_results = watson.filter(School, form.data['query'])
            return render(request, 'school/search.html', {'form': form, 'results':search_results})
    else:
        form = SchoolSearchForm()
    
    return render(request, 'school/search.html', {'form': form})

def school(request, school_id):
    try:
        school = School.objects.get(id=school_id)
    except:
        return redirect('not_found')

    try:
        d1team = Team.objects.get(school=school, division="Division 1")
    except:
        d1team = None

    try:
        d2teams = Team.objects.filter(school=school, division="Division 2")
    except:
        d2teams = None

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

    d1team_roster = Player.objects.filter(team=d1team)
    
    return render(request, 'school/school.html', {'team': team, 'can_join': can_join, 'can_create': can_create, 'school': school, 'd1team': d1team, 'd1team_roster': d1team_roster, 'd2teams': d2teams})

def hub(request):
    leaderboard = get_hub_leaderboard()
    return render(request, 'hub.html', {'leaderboard': leaderboard})

def league(request):
    return render(request, 'league.html')

def one_payment(request):
    return div_one_payment()
def two_payment(request):
    return div_two_payment()
def one_sub_payment(request):
    return div_one_sub_payment()
def two_sub_payment(request):
    return div_two_sub_payment()

def payment_return(request):
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    
    # ID of the payment. This ID is provided when creating payment.
    paymentId = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = paypal.Payment.find(paymentId)

    # PayerID is required to approve the payment.
    if payment.execute({"payer_id": payer_id}):  # return True or False
        newPayment = Payment(name=request.user,paymentid=paymentId, payerid=payer_id ,user=user)
        newPayment.save()
        player.has_paid = 1
        player.save()

        print(paymentId + " " + payer_id)
        return redirect('index')
    else:
        print('error')
        return redirect('index')
    