from django import forms
from django.contrib.auth.models import User
#from captcha.fields import CaptchaField

class ManageAccount(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	username = forms.CharField(max_length=100)
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	class Meta:
		model=User
		fields=('password','username','first_name','last_name',)


class SignupForm(forms.Form):
#	captcha = CaptchaField(required=True)
	first_name = forms.CharField(max_length=100, label='First Name')
	last_name = forms.CharField(max_length=100, label='Last Name')
	def signup(self, request, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()

