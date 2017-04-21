from django import forms


class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()

class People(forms.Form):
    a=forms.CharField(max_length=20)
    b=forms.CharField(max_length=20)
