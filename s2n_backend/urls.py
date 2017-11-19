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

from django.conf.urls import (url, include)
from rest_framework import routers # rest_framework_nested ?
from django.contrib import admin
# from login.views import *
from pantry.views import *
from rest_framework_jwt.views import verify_jwt_token

router = routers.DefaultRouter()
router.register(prefix='api/foods', viewset=FoodItemViewSet)
router.register(prefix='api/recipes', viewset=RecipeViewSet)
router.register(prefix='api/cuisines', viewset=CuisineViewSet)
router.register(prefix='api/courses', viewset=CourseViewSet)
router.register(prefix='api/pantry', viewset=PantryItemViewSet, base_name='pantry')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.jwt')),
    url(r'^api-token-verify/', verify_jwt_token),
]
