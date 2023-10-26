from django import forms
from .models import UserInput

class UserInputForm(forms.ModelForm):
	class Meta:
		model = UserInput
		fields = ['topic']
