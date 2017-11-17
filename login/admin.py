from django.contrib import admin
from .models import Ingredient
from .models import Account
from .models import AccountManager


#register models here
admin.site.register(Ingredient)
admin.site.register(Account)
admin.site.register(AccountManager)
