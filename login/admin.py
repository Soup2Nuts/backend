from django.contrib import admin
from django.contrib.auth import models

from login.models import (Account, AccountManager)




#register models here
admin.site.register(Account)
#admin.site.register(AccountManager)
