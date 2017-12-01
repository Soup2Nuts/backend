from django.test import TestCase, Client
from django.core import management
from .models import *
from .utils import *
import time
from rest_framework_jwt import utils

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
    def test_get_all_valid_recipes_helper_1(self):
        unavailable_foods = FoodItem.objects.none()
        result = get_all_valid_recipes_helper(unavailable_foods=unavailable_foods, cuisines=None, courses=None)
        self.assertQuerysetEqual(result, map(repr, Recipe.objects.all()), ordered=False)

    #Tests get_all_valid_recipes_helper
    #User has all foods in pantry and has filtered results only by courses
    def test_get_all_valid_recipes_helper_2(self):
        courses = Course.objects.filter(name__in=['Lunch', 'Dinner', 'American'])
        cuisines = None
        unavailable_foods = FoodItem.objects.none()
        result = get_all_valid_recipes_helper(unavailable_foods=unavailable_foods, cuisines=cuisines, courses=courses)
        self.assertQuerysetEqual(result, map(repr, Recipe.objects.filter(courses__name__in=courses)), ordered=False)

    #Tests get_all_valid_recipes_helper
    #User has all foods in pantry and has filtered results only by cuisines
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

class SearchView(TestCase):

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

    #Test response for a user without a token
    def test_search_recipes1(self):
        response = self.client.get('/api/search/', HTTP_AUTHORIZATION='not a real token')
        self.assertEqual(response.status_code, 401)

    #Test response for a user with a token
    def test_search_recipes2(self):
        response = self.client.get('/api/search/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, 200)

    #Test response time for a user with a token and every FoodItem in their pantry
    #High stress test
    def test_search_recipes3(self):
        all_foods = FoodItem.objects.all()
        for f in all_foods:
            PantryItem.objects.create(owner = self.user, item=f)
        search_time = time.time()
        response = self.client.get('/api/search/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, 200)
        t = time.time() - search_time
        print ("Search Time: %s: %.3f"%(self.id(), t))
