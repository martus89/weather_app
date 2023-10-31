from django import forms


class SearchingForm(forms.Form):
    city_input = forms.CharField()


