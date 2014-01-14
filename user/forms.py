from django import forms
from user.models import Owner
from django.contrib.localflavor.us.forms import USZipCodeField

class EditInfoForm(forms.ModelForm):
	"""
	Form used for editing a user's information
	"""
	class Meta:
		model = Owner
		fields = ('fname', 'lname', 'address')

class EditZipCodeForm(forms.ModelForm):
	"""
	Form used to edit a user's zipcode
	Zipcode will not be allowed to change if a user has
	currently borrowed/loaned tools or tools in a public shed
	"""
	zipcode = USZipCodeField()
	class Meta:
		model = Owner
		fields = ('zipcode',)
