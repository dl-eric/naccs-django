from django import forms
from django.core.exceptions import ValidationError

from .models import Team, School, Player


class SchoolSearchForm(forms.Form):
    query = forms.CharField(label="College Name", min_length=6,
                            widget=forms.TextInput(attrs={'placeholder': 'Search'}))

class JoinTeamForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.teams = kwargs.pop('teams')
        teams_tuple = []
        for team in self.teams:
            teams_tuple.append((team, team))
        super().__init__(*args, **kwargs)
        self.fields['teams'].widget = forms.Select(choices=teams_tuple)

    def clean(self):
        cleaned_data = super().clean()

        selected_team = cleaned_data.get('teams')

        for team in self.teams:
            if team.name == selected_team:
                # Check password
                if team.join_password == cleaned_data.get('password'):
                    return cleaned_data
                else:
                    raise ValidationError('Wrong password')

        raise ValidationError('Team not found')

    teams = forms.CharField(label="Team")
    password = forms.CharField(label="Join Password", widget=forms.PasswordInput())

class EditTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'join_password')

class EditPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('role',)

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'division', 'join_password')

    def __init__(self, *args, **kwargs):
        self.school_id = kwargs.pop('school_id')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        division = cleaned_data.get('division')
        if division != 'Division 1' and division != 'Division 2':
            raise ValidationError("Division Malformed")

        school = School.objects.get(id=self.school_id)

        if division == 'Division 1':
            # Check if there already exists a D1 team
            if Team.objects.filter(school=school, division='Division 1').exists():
                raise ValidationError('A D1 team already exists for that school!')

        if division == 'Division 2':
            # Check if there already exists a D2 team
            if Team.objects.filter(school=school, division='Division 2').exists():
                raise ValidationError('A D2 team already exists for that school!')
        
        # Check if team name is already taken
        if Team.objects.filter(name=cleaned_data.get('name')).exists():
            raise ValidationError('A team with that name already exists!')

        return cleaned_data

    name = forms.CharField(label="Team Name", required=True)
    join_password = forms.CharField(label="Join Password", required=True, widget=forms.PasswordInput())
    division = forms.ChoiceField(label="Division", required=True, choices=[("Division 1", "Division 1"), ("Division 2", "Division 2")])