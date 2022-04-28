from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import *
from django import forms 
from django.forms import DateField, widgets
'''
we need to create this class as we need to change the model 
to our custom user model 'MyUser'
'''

#this form is used to CREATE A USER (eg REGISTER FORM)
class CustomUserCreationForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):
        model = MyUser
        #fields = UserCreationForm.Meta.fields + ('letsgo',)
        fields = ['username', 'email','city','dob', 'password1', 'password2',]
        widgets = {
   'dob': widgets.DateInput(attrs = {
      'type': 'date'
   })
}

class addHobbiesForm(forms.ModelForm):

    class Meta:
        model = Hobby
        
        fields='__all__'

class viewHobbiesForm(forms.ModelForm):

    class Meta:
        model = Hobby
        
        fields = '__all__'

