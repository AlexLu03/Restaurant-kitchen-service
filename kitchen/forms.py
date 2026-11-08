from django import forms


class CookSearchForm(forms.Form):
    username = forms.CharField(
        required=False,
        label='Username',
    )
    min_experience = forms.IntegerField(
        required=False,
        min_value=0,
        label='Minimum experience',
    )
    max_experience = forms.IntegerField(
        required=False,
        min_value=0,
        label='Maximum experience',
    )
