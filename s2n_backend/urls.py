"""s2n_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
<<<<<<< HEAD
from django.conf.urls import (url, include)
from rest_framework import routers # rest_framework_nested ?
from django.contrib import admin
from login.views import *

router = routers.DefaultRouter()
router.register(r'users', viewset=AccountViewSet)
=======
from django.conf.urls import url, include
from rest_framework import routers
from django.contrib import admin
from pantry.views import *


from backend import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(prefix='foods', viewset=FoodItemViewSet)
>>>>>>> branch-katie-test

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
<<<<<<< HEAD
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
=======
>>>>>>> branch-katie-test
]
