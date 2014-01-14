from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

class IntegerRangeField(models.IntegerField):
        def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
                self.min_value, self.max_value = min_value, max_value
                models.IntegerField.__init__(self, verbose_name, name, **kwargs)
        def formfield(self, **kwargs):
                defaults = {'min_value': self.min_value, 'max_value': self.max_value}
                defaults.update(kwargs)
                return super(IntegerRangeField, self).formfield(**defaults)

class OwnerManager(BaseUserManager):
    def create_user(self, email, fname, lname, address, zipcode, password=None):
        """
        Creates a new user, requires all arguments
        to participate in ToolShare
        """
        if not email:
            raise ValueError('Users must have a valid email address')
        if not fname:
            raise ValueError('Users must enter their first name')
        if not lname:
            raise ValueError('Users must enter their last name')
        if not address:
            raise ValueError('Users must have an address to share or borrow tools')
        if not zipcode:
            raise ValueError('Zipcode determines what tools are available')

        user=self.model(
            email=OwnerManager.normalize_email(email),
            fname=fname,
            lname=lname,
            address=address,
            zipcode=zipcode,
            date_joined=timezone.now(),
            password=password,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fname, lname, address, zipcode, password):
        """
        Creates and saves a superuser
        """
        user=self.create_user(
            email,
            fname=fname,
            lname=lname,
            address=address,
            zipcode=zipcode,
            password=password
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user

class Owner(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email Address', max_length=100, unique=True, db_index=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=60)
    address = models.CharField(max_length=150)
    date_joined = models.DateField(auto_now_add=True)
    zipcode = IntegerRangeField(min_value=00000,max_value=99999)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = OwnerManager()

    lend_counter = models.IntegerField(default=0)
    borrow_counter = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname', 'address', 'zipcode']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.fname

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        return True 

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin