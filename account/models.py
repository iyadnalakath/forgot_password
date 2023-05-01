from django.db import models
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.template.loader import render_to_string
import string
import random
import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager as AbstractUserManager
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
# Create your models here.




class UserManager(AbstractUserManager):
  pass

class Account(AbstractUser):

    user_admin = "admin"
    user_customer = "customer"

    user_choices = [
        (user_customer, "customer"),
        (user_admin, "admin"),
    ]

    email = models.EmailField(verbose_name="email",unique=True)
    username = models.CharField(max_length=60, unique=True,null=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False, null=True, blank=True)
    is_superuser = models.BooleanField(default=False, null=True, blank=True)
    
    role = models.CharField(max_length=30,null=True,blank=True,choices=user_choices,default=user_customer)
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "email",
    ]

 
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)      




# Sure! @receiver(post_save, sender=settings.AUTH_USER_MODEL) is a decorator in Django that listens to a post_save signal (which gets triggered every time an object is saved) for the settings.AUTH_USER_MODEL model (which is the user model defined in the Django settings).

# In the context of the code you shared earlier, this decorator is used to automatically create a Token object for a user every time a new user is created.




def password_generater(length):
    length = 8
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    rnd = random.SystemRandom()
    return(''.join(rnd.choice(chars) for i in range(length)))

class PasswordRest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, null=True, blank=True)



   # def __str__(self) -> str:
    #     return self.username

    # def __str__(self) -> str:
    #     return self.full_name

    # def __str__(self):
    #     return self.email

    # def __str__(self) -> str:
    #     return self.team_name

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    # def has_module_perms(self, app_label):
    #     return True
    