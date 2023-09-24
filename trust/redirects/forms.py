from django import forms

from .models import Connect

class LinkForm(forms.Form):
    #code = forms.CharField(label='Код активации',)
    link = forms.CharField(label='URL редиректа',)
    count_link = forms.IntegerField(
        label='Кол-во редиректов',
        min_value=1,
        max_value=4200,
    )


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Connect
        fields = ('feedback',)


class CheckEmailForm(forms.Form):
    emails = forms.CharField(label='Список emails',
                             widget=forms.Textarea)