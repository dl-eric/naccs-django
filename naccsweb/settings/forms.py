from django import forms
from django.core.exceptions import ValidationError

from .models import GraduateFormModel, HighSchoolFormModel
from .schools import get_schools

class CollegeForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.schools = kwargs.pop('schools')
        schools_tuple = []
        for school in sorted(self.schools):
            schools_tuple.append((school, school))
        super().__init__(*args, **kwargs)
        self.fields['college'].widget = forms.Select(choices=schools_tuple)

    def clean(self):
        cleaned_data = super().clean()

        email_suffix = cleaned_data.get('email').split('@')[1]
        valid_emails = self.schools.get(cleaned_data.get('college'))
        valid = False
        for email in valid_emails:
            if email_suffix == email:
                valid = True
                break

        if not valid:
            raise ValidationError('Invalid College Email')

        return cleaned_data    

    college = forms.CharField(label="College Name")
    email   = forms.EmailField(label="College Email")

class GraduateForm(forms.ModelForm):
    class Meta:
        model = GraduateFormModel
        fields = ('college', 'grad_date', 'proof', 'other')
        exclude = ['user']

    college    = forms.CharField(label="College")
    grad_date  = forms.DateField(label="Graduation Date", help_text="MM/DD/YY")
    proof      = forms.FileField(label="Proof, such as transcript or diploma")
    other      = forms.CharField(label="Other Information", help_text="Optional", widget=forms.Textarea(attrs={'rows': 5}), required=False)

class HighSchoolForm(forms.ModelForm):
    class Meta:
        model = HighSchoolFormModel
        fields = ('highschool', 'college', 'grad_date', 'proof', 'other')
        exclude = ['user']

    highschool = forms.CharField(label="Current Highschool")
    grad_date  = forms.DateField(label="Graduation Date", help_text="MM/DD/YY")
    college    = forms.CharField(label="Future College")
    proof      = forms.FileField(label="Acceptance Letter")
    other      = forms.CharField(label="Other Information", help_text="Optional", widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}), required=False)

class MilitaryForm(forms.Form):
    # TODO
    pass