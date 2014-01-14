from django import forms
from django.core.exceptions import ValidationError
from shed.models import Shed
from django.db import models

from tools.models import Tool

class BasicToolForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
	    super(BasicToolForm, self).__init__(*args, **kwargs)

	    #for key in self.fields:
	    self.fields['image'].required = False

class ToolForm(BasicToolForm):
    class Meta:
        model = Tool
        fields = ('name', 'description', 'shed_id', 'return_date_limit', 'image')



class BorrowForm(forms.Form):
	return_date = forms.DateField()
	msg = forms.CharField(max_length=200, required=False)

class DenyForm(forms.Form):
	reason = forms.CharField(max_length=200)