from django import forms
from django.contrib.auth.models import User
from .models import Events



class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

class EventsForm(forms.ModelForm):
   class Meta:
       model = Events
       fields = "__all__"
       #exclude = ['added_by']

       widgets = {
           'date': forms.DateInput(attrs={'type': 'date'}),
           'time': forms.TimeInput(attrs={'type': 'time'}),
       }
