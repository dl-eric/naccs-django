from django import forms
from django.core.exceptions import ValidationError

from .models import Team, School, Player, Division


class SchoolSearchForm(forms.Form):
    query = forms.CharField(label="College Name", min_length=4,
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

        school = School.objects.get(id=self.school_id)
        if cleaned_data["division"].name == 'Division 1':
            # Check if there already exists a D1 team
            team = Team.objects.filter(school=school, division__name="Division 1").count()
            if team > 0:
                raise ValidationError('A D1 team already exists for that school!')
        
        # Check if team name is already taken
        if Team.objects.filter(name=cleaned_data.get('name')).exists():
            raise ValidationError('A team with that name already exists!')

        return cleaned_data

    name = forms.CharField(label="Team Name", required=True)
    join_password = forms.CharField(label="Join Password", required=True, widget=forms.PasswordInput())
    division = forms.ModelChoiceField(queryset=Division.objects.all(), label="Division", required=True, empty_label=None)