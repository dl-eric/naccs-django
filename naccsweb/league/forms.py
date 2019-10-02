from django import forms


class SchoolSearchForm(forms.Form):
    query = forms.CharField(label="College Name", min_length=6,
                            widget=forms.TextInput(attrs={'placeholder': 'Search'}))