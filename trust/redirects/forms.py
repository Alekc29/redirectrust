from django import forms


class LinkForm(forms.Form):
    code = forms.CharField(max_length=20)
    link = forms.CharField()
    count_link = forms.IntegerField()
