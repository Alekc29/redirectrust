from django import forms


class LinkForm(forms.Form):
    code = forms.CharField(label='Код активации',)
    link = forms.CharField(label='URL редиректа',)
    count_link = forms.IntegerField(
        label='Кол-во редиректов',
        min_value=1,
        max_value=1000,
    )
