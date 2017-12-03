from django.test import TestCase, Client
from django.core import management
from .models import *
from .utils import *
import time
from rest_framework_jwt import utils
from unittest import skipIf
from django.utils.http import urlencode

#Set to False to include stress tests
fast = False

def setup():
    management.call_command('loaddata', 'initial_data.json', verbosity=0)

def teardown():
    management.call_command('flush', verbosity=0, interactive=False)

class SearchUtilTests(TestCase):

    #Used to time individual tests
    def setUp(self):
        self.startTime = time.time()

    #Used to time individual tests
    def tearDown(self):
        t = time.time() - self.startTime
        print ("%s: %.3f"%(self.id(), t))

    #Tests get_all_valid_recipes_helper
    #User has every food item in their pantry and is not filtering by cuisines or courses
    @skipIf(fast, 'Stress tests are slow')
    def test_get_all_valid_recipes_helper_1(self):
        unavailable_foods = FoodItem.objects.none()
        result = get_all_valid_recipes_helper(unavailable_foods=unavailable_foods, cuisines=None, courses=None)
        self.assertQuerysetEqual(result, map(repr, Recipe.objects.all()), ordered=False)

    #Tests get_all_valid_recipes_helper
    #User has all foods in pantry and has filtered results only by courses
    @skipIf(fast, 'Stress tests are slow')
    def test_get_all_valid_recipes_helper_2(self):
        courses = Course.objects.filter(name__in=['Lunch', 'Dinner', 'American'])
        cuisines = None
        unavailable_foods = FoodItem.objects.none()
        result = get_all_valid_recipes_helper(unavailable_foods=unavailable_foods, cuisines=cuisines, courses=courses)
        self.assertQuerysetEqual(result, map(repr, Recipe.objects.filter(courses__name__in=courses)), ordered=False)

    #Tests get_all_valid_recipes_helper
    #User has all foods in pantry and has filtered results only by cuisines
    @skipIf(fast, 'Stress tests are slow')
    def test_get_all_valid_recipes_helper_3(self):
        courses = None
        cuisines = Cuisine.objects.exclude(name='American')
        unavailable_foods = FoodItem.objects.none()
        result = get_all_valid_recipes_helper(unavailable_foods=unavailable_foods, cuisines=cuisines, courses=courses)
        correct = Recipe.objects.filter(cuisines__name__in=cuisines).distinct()
        self.assertEqual(len(result), len(correct))
        self.assertQuerysetEqual(result, map(repr, correct), ordered=False)

    #Tests get_all_valid_recipes_helper
    #User has all foods in pantry and has filtered results by both courses and cuisines
    @skipIf(fast, 'Stress tests are slow')
    def test_get_all_valid_recipes_helper_4(self):
        courses = Course.objects.exclude(name='Breakfast')
        cuisines = Cuisine.objects.filter(name='American')
        unavailable_foods = FoodItem.objects.none()
        result = get_all_valid_recipes_helper(unavailable_foods=unavailable_foods, cuisines=cuisines, courses=courses)
        correct = Recipe.objects.filter(courses__name__in=courses, cuisines__name__in=cuisines).distinct()
        self.assertEqual(len(result), len(correct))
        self.assertQuerysetEqual(result, map(repr, correct), ordered=False)

    #Tests get_all_valid_recipes_helper
    #User has no foods in their pantry
    def test_get_all_valid_recipes_helper_5(self):
        unavailable_foods = FoodItem.objects.all()
        result = get_all_valid_recipes_helper(unavailable_foods=unavailable_foods, cuisines=None, courses=None)
        self.assertQuerysetEqual(result, map(repr, Recipe.objects.none()), ordered=False)

class ModelTest(TestCase):

    #Used to time individual tests
    def setUp(self):
        self.startTime = time.time()

    #Used to time individual tests
    def tearDown(self):
        t = time.time() - self.startTime
        print ("%s: %.3f"%(self.id(), t))

    #Test test_recipe
    #Test whether a recipe model prints correctly
    def test_recipe(self):
        recipe = Recipe.objects.create(title='Test recipe', source='www.recipe.com')
        recipe.cuisines=Cuisine.objects.all()[:1]
        recipe.courses=Course.objects.all()[:1]
        recipe.ingredients=Ingredient.objects.all()[:3]
        made_string = 'Title: ' + recipe.title + '\n'
        made_string += 'Source: ' + recipe.source + '\n'
        made_string += 'Cuisines: ' + str(recipe.cuisines.all()) + '\n'
        made_string += 'Courses: ' + str(recipe.courses.all()) + '\n'
        made_string += 'Ingredients:\n'
        for i in recipe.ingredients.all():
            made_string += str(i) + '\n'
        test_string = ""
        test_string += str(recipe)
        self.assertEqual(test_string, made_string)

class PantryView(TestCase):

    #Used to time individual tests and add a valid token to the auth header
    def setUp(self):
        self.client = Client()
        self.username = 'bigboi99'
        self.email = 'bigboi99@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        payload = utils.jwt_payload_handler(self.user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'Bearer {0}'.format(token)
        self.startTime = time.time()

    #Used to time individual tests
    def tearDown(self):
        t = time.time() - self.startTime
        print ("%s: %.3f"%(self.id(), t))
        self.user.delete()

    #Tests test_pantry
    #Test response to access the pantry for user without a token
    def test_pantry_1(self):
        response = self.client.get('/api/pantry/', HTTP_AUTHORIZATION='not a real token')
        self.assertEqual(response.status_code, 401)

    #Tests test_pantry
    #Test response to access the pantry for user with a token
    def test_pantry_2(self):
        response = self.client.get('/api/pantry/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, 200)

    #Tests test_favorites
    #Test response to access favorites for user without a token
    def test_favorites_1(self):
        response = self.client.get('/api/favorites/', HTTP_AUTHORIZATION='not a real token')
        self.assertEqual(response.status_code, 401)

    #Tests test_favorites
    #Test response to access favorites for user with a token
    def test_favorites_2(self):
        response = self.client.get('/api/favorites/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, 200)

    #Tests test_pantry_put
    #Test response to add item to the pantry for user without a token
    def test_pantry_put_1(self):
        response = self.client.post('/api/pantry/put', {'food_name': 'sugar'}, HTTP_AUTHORIZATION='not a real token')
        self.assertEqual(response.status_code, 401)

    #Tests test_pantry_put
    #Test response to add item to the pantry for user with a token
    def test_pantry_put_2(self):
        response = self.client.post('/api/pantry/put', {'food_name': 'sugar'}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, 200)

    #Tests test_favorites_add
    #Test response to add a recipe to favorites for user without a token
    def test_favorites_add_1(self):
        response = self.client.post('/api/favorites/put', {'recipe_name': 'Apple Cranberry Salad Toss'}, HTTP_AUTHORIZATION='not a real token')
        self.assertEqual(response.status_code, 401)

    #Tests test_favorites_add
    #Test response to add a recipe to favorites for user with a token
    def test_favorites_add_2(self):
        response = self.client.post('/api/favorites/put', {'recipe_name': 'Apple Cranberry Salad Toss'}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, 201)

    #Tests test_pantry_delete
    #Test response to delete an item from the pantry for user without a token
    def test_pantry_delete_1(self):
        all_foods = FoodItem.objects.all()
        for f in all_foods:
            PantryItem.objects.create(owner = self.user, item=f)
        response = self.client.delete('/api/pantry/delete?food_name=black+beans', HTTP_AUTHORIZATION='not a real token')
        self.assertEqual(response.status_code, 401)

    #Tests test_pantry_delete
    #Test response to delete an item from the pantry for user with a token
    def test_pantry_delete_2(self):
        all_foods = FoodItem.objects.all()
        for f in all_foods:
            PantryItem.objects.create(owner = self.user, item=f)
        response = self.client.delete('/api/pantry/delete?food_name=black+beans', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, 204)

    #Tests test_favorites_delete
    #Test response to delete a recipe from favorites for user without a token
    def test_favorites_delete_1(self):
        all_recipes = Recipe.objects.all()
        for f in all_recipes:
            FavoriteRecipe.objects.create(owner = self.user, recipe=f)
        response = self.client.delete('/api/favorites/delete?recipe_name=Apple+Chunk+Cake', HTTP_AUTHORIZATION='not a real token')
        self.assertEqual(response.status_code, 401)

    #Tests test_favorites_delete
    #Test response to delete a recipe from favorites for user with a token
    def test_favorites_delete_2(self):
        all_recipes = Recipe.objects.all()
        for f in all_recipes:
            FavoriteRecipe.objects.create(owner = self.user, recipe=f)
        response = self.client.delete('/api/favorites/delete?recipe_name=Apple+Chunk+Cake', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, 204)

class SearchViewTests(TestCase):

    #Used to time individual tests and add a valid token to the auth header
    def setUp(self):
        self.client = Client()
        self.username = 'john8888'
        self.email = 'john8888@example.com'
        self.user = User.objects.create_user(self.username, self.email)
        payload = utils.jwt_payload_handler(self.user)
        token = utils.jwt_encode_handler(payload)
        self.auth = 'Bearer {0}'.format(token)
        self.startTime = time.time()

    #Used to time individual tests
    def tearDown(self):
        t = time.time() - self.startTime
        print ("%s: %.3f"%(self.id(), t))
        self.user.delete()

    #Test test_search_recipes
    #Test response for a user without a token
    def test_search_recipes_1(self):
        response = self.client.get('/api/search/', HTTP_AUTHORIZATION='not a real token')
        self.assertEqual(response.status_code, 401)

    #Test test_search_recipes
    #Test response for a user with a token
    def test_search_recipes_2(self):
        response = self.client.get('/api/search/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, 200)

    #Test test_search_recipes
    #Test response time for a user with a token and every FoodItem in their pantry
    #High stress test
    @skipIf(fast, 'Stress tests are slow')
    def test_search_recipes_3(self):
        all_foods = FoodItem.objects.all()
        for f in all_foods:
            PantryItem.objects.create(owner = self.user, item=f)
        search_time = time.time()
        response = self.client.get('/api/search/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, 200)
        t = time.time() - search_time
        print ("Search Time: %s: %.3f"%(self.id(), t))
