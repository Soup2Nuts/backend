from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)

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
		account = self.createUser(username, password)

		account.isAdmin	= True;
		account.save()

		return account

class Account(AbstractBaseUser):
	username = models.CharField(max_length=40, unique=True)

	firstName = models.CharField(max_length=40, blank=True)
	lastName = models.CharField(max_length=40, blank=True)

	isAdmin = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)

	updated_at = models.DateTimeField(auto_now=True)	

	objects = AccountManager()

	USERNAME_FIELD = 'username'
	# REQUIRED_FIELDS = ['username']

	def __str__(self):
		return self.username

	def get_full_name(self):
		return ' '.join([self.firstName, self.lastName])

