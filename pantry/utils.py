from .models import *
from rest_framework_jwt.utils import jwt_decode_handler
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from fractions import Fraction
from django.http import HttpResponse

#Decode the user from the request's header
def get_user(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        token = token.split(' ', 1)[1]
        user_id = jwt_decode_handler(token)['user_id']
        return User.objects.get(pk=user_id)
    except:
        #raise PermissionDenied("Request has an invalid or expired token")
        return HttpResponse(status=401)

#Returns a queryset of all FoodItems in the user's pantry
def get_foods_in_pantry(user):
    pantry = user.pantry.all()
    q = Q(pantryitem__in = pantry)
    return FoodItem.objects.filter(q)

#Returns a queryset of all FoodItems not in the user's pantry
def get_foods_not_in_pantry(user):
    pantry = user.pantry.all()
    q = ~Q(pantryitem__in = pantry)
    return FoodItem.objects.filter(q)

#Returns all substitutions that can be made from the user's pantry
def get_valid_substitutions(user):
    unavailable_foods = get_foods_not_in_pantry(user)
    q = ~Q(substitute_foods__substitute_food__in = unavailable_foods)
    return Substitution.objects.filter(q)

#Returns all foods items produced by valid substitutions from the user's pantry or in the user's pantry
def get_all_available_foods(user):
    pantry = user.pantry.all()
    subs = get_valid_substitutions(user)
    return FoodItem.objects.filter(Q(pantryitem__in = pantry)|Q(substitutions__in = subs)).distinct()

#Returns all foods items which cannot be produced by valid substitutions from the user's pantry and are not in the user's pantry
def get_all_unavailable_foods(user):
    pantry = user.pantry.all()
    subs = get_valid_substitutions(user)
    return FoodItem.objects.filter(~Q(pantryitem__in = pantry)&~Q(substitutions__in = subs)).distinct()

#Returns all recipes containing only foods items produced by valid substitutions from the user's pantry or in the user's pantry
#and are at least of one of specified cuisines and at least one of the specified courses
def get_all_valid_recipes(user, cuisines=None, courses=None):
    unavailable_foods = get_all_unavailable_foods(user)
    q = ~Q(ingredients__name__in = unavailable_foods)
    if(cuisines==None and courses==None):
        return Recipe.objects.filter(q)
    if(cuisines==None):
        return Recipe.objects.filter(q, courses__name__in=courses)
    if(courses==None):
        return Recipe.objects.filter(q, cuisines__name__in=cuisines)
    return Recipe.objects.filter(q, cuisines__name__in=cuisines, courses__name__in=courses)

#Returns a queryset of all of the substitutions needed to be made for the specified recipe to be made from the FoodItem in the specified user's pantry
def get_substitutions_made(user, recipe):
    pantry = user.pantry.all()
    item_in_recipe = Q(ingredient__in = recipe.ingredients.all())
    item_in_pantry = Q(pantryitem__in = pantry)
    missing_foods = FoodItem.objects.filter(item_in_recipe & ~item_in_pantry)
    valid_subs = get_valid_substitutions(user)
    distinct_subs = []
    for missing_food in missing_foods:
        temp = valid_subs.filter(original_food=missing_food)
        if(len(temp)<=0):
            print('"%s" can not make recipe "%s"'%user %recipe.title)
            return None
        distinct_subs.append(temp[0])
    return distinct_subs

#Input: array of substitutions and a collection ingredients in their final order
#Returns the actual substitutions made to a set of ingredients
def get_real_substitutions(substitutions, ingredients):
    real_subs = {}
    for i in range(0, len(ingredients)):
        for s in range(0, len(substitutions)):
            if ingredients[i]['name']==substitutions[s].original_food.name:
                subs = []
                for substitute_food in substitutions[s].substitute_foods.all():
                    sub = {}
                    info = ingredients[i]['quantity'].split(maxsplit= 1)
                    frac = Fraction(info[0])
                    frac2 = Fraction(str(substitute_food.ratio))
                    sub['quantity'] = str(frac*frac2)
                    if len(info)>=2:
                        sub['quantity']+= ' ' + str(info[1])
                    sub['name'] = str(substitute_food.substitute_food.name)
                    subs.append(sub)
                if(len(subs) != 0):
                    real_subs[i]=subs
                break
    return real_subs
