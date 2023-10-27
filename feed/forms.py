from django import forms
from .models import UserInput

class UserInputForm(forms.ModelForm):
	"""
	Form for user input related to the 'UserInput' model.
	"""
	topic = forms.CharField(
		label="topic",
		widget=forms.TextInput(attrs={"class": "block w-full rounded-md border-0 py-1.5 pl-7 pr-20 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}),
	)

	class Meta:
		model = UserInput
		fields = ['topic']
