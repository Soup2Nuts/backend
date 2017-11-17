from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models

class AccountManager(BaseUserManager):
	def createUser(self, username, password=None, **kwargs):
		if not username:
			raise ValueError('Users must have a valid username')

		# if not kwargs.get('username'):
			# raise ValueError('Users must have a valid username')

		account = self.model(
			username = self.username # , username = kwargs.get('username')
		)

		account.set_password(password)
		account.save()

		return account

	def createSuperUser(self, username, password, **kwargs):
		account = self.createUser(username, password, **kwargs)

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
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
    	return self.username

    def getFullName(self):
    	return ' '.join([self.firstName, self.lastName])

class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"

    def __unicode__(self):
        return self.name

