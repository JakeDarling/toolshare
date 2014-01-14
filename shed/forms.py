from django import forms
from django.core.exceptions import ValidationError

from shed.models import Shed

class ShedForm(forms.ModelForm):
    class Meta:
        model = Shed
        fields = ('name', 'address_one', 'address_two', 'zipcode', 'private')

class EditShedForm(forms.ModelForm):
	class Meta:
		model = Shed
		fields = ('name', 'address_one', 'address_two')