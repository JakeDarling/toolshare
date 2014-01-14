from django.db import models
from django.forms import ModelForm

class IntegerRangeField(models.IntegerField):
        def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
                self.min_value, self.max_value = min_value, max_value
                models.IntegerField.__init__(self, verbose_name, name, **kwargs)
        def formfield(self, **kwargs):
                defaults = {'min_value': self.min_value, 'max_value': self.max_value}
                defaults.update(kwargs)
                return super(IntegerRangeField, self).formfield(**defaults)

class Tool(models.Model):
        #users = models.ForeignKey(User)
    
        name = models.CharField(max_length=100)
        owner_id = models.IntegerField()
        owner_string = models.CharField(max_length=100)
        borrower_id = models.IntegerField()
        borrower_string = models.CharField(max_length=100)
        shed_id = models.IntegerField()
        shed_string = models.CharField(max_length=100)
        zipcode = models.IntegerField()
        availability = models.IntegerField(max_length=1) #0 for unavailable 1 for available. 2 for in request. 3 for not returned. 4 for user-set unavailable.
        description = models.CharField(max_length=1000)
        creation_date = models.DateField('%m/%d/%Y')
        return_date = models.DateField('%m/%d/%Y')
        return_date_limit = IntegerRangeField(min_value=1, max_value=30)

        image = models.FileField(upload_to='images', default='images/default.png')
        usage_count = models.IntegerField()

        def __str__(self):
                return "ToolID:" + str(self.id) + " Name:" + str(self.name) + " Location:" + str(self.location)
        
