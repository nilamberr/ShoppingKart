from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    password1= forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2= forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email= forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels = {'email':'email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}

class LoginForm(AuthenticationForm):
    username= forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    password= forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','password']

class PasswordChange(PasswordChangeForm):
    old_password= forms.CharField(label=("Old Password"),strip=False,widget=
        forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,
        'class':'form-control'}))
    new_password1=forms.CharField(label=("New Password"),strip=False,widget=
        forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),
        help_text=password_validation.password_validators_help_text_html())
    new_password2= forms.CharField(label=("Confirm New Password"),strip=False,widget=
        forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class PasswordReset(PasswordResetForm):
    email= forms.EmailField(label=("Email"),max_length=250,widget=forms.EmailInput(attrs=
        {'autocomplete':'email','class':'form-control'}))

class SetPassword(SetPasswordForm):
    new_password1=forms.CharField(label=("New Password"),strip=False,widget=
        forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),
        help_text=password_validation.password_validators_help_text_html())
    new_password2= forms.CharField(label=("Confirm New Password"),strip=False,widget=
        forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
    
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','locality','city','zipcode','state']
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),
                 'locality':forms.TextInput(attrs={'class':'form-control'}),
                 'city':forms.TextInput(attrs={'class':'form-control'}),
                 'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
                 'state':forms.TextInput(attrs={'class':'form-control'})}