from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class AccountManager(BaseUserManager):
	def create_user(self, username, password=None):
		if not username:
			raise ValueError('Users must have a valid username')

		account = self.model(
			username = username
		)

		account.set_password(password)
		account.save()

		return account

	def create_superuser(self, username, password):
		account = self.create_user(username, password)

		account.is_admin	= True;
		account.is_superuser = True;
		account.is_staff = True;
		account.save()

		return account

class Account(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=40, unique=True)

	firstName = models.CharField(max_length=40, blank=True)
	lastName = models.CharField(max_length=40, blank=True)

	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	date_joined = models.DateTimeField(auto_now_add=True)

	last_login = models.DateTimeField(auto_now=True)	

	objects = AccountManager()

	USERNAME_FIELD = 'username'
	#REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.username

	def get_full_name(self):
		return ' '.join([self.firstName, self.lastName])

	def get_short_name(self):
		return self.firstName

	def __unicode__(self):
	    return self.username
