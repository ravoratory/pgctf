from django import forms


class CheckFlagForm(forms.Form):
    flag = forms.CharField(label="Flag", max_length=200, widget=forms.TextInput(attrs={"placeholder": "pgctf{?????}"}))
