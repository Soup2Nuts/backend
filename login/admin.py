from django.contrib import admin
from .models import Account
from .models import AccountManager


#register models here
admin.site.register(Account)
admin.site.register(AccountManager)
