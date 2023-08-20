from django.test import TestCase

from kitchen.models import DishType, Cook
from kitchen.forms import (
    CookCreationForm,
    DishForm,
    CookSearchForm,
    DishSearchForm,
    DishTypeSearchForm,
)


class CookCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "email": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "years_of_experience": 5,
            "email": "john@gmail.com",
            "first_name": "John",
            "last_name": "Doe",
            "photo": None,
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_invalid_form(self):
        form_data = {
            "email": "",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "years_of_experience": 5,
            "first_name": "John",
            "last_name": "Doe",
            "photo": None,
        }
        form = CookCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertNotEqual(form.cleaned_data, form_data)


class DishFormTest(TestCase):
    def test_valid_form(self):
        dish_type = DishType.objects.create(name="Main Course")
        cook1 = Cook.objects.create(
            email="cook1", first_name="John", last_name="Doe"
        )
        cook2 = Cook.objects.create(
            email="cook2", first_name="Tim", last_name="Black"
        )

        form_data = {
            "name": "Delicious Dish",
            "description": "A tasty dish",
            "price": 10.99,
            "dish_type": dish_type.id,
            "cooks": [cook1.id, cook2.id],
            "dish_photo": None,
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "name": "",
            "description": "A tasty dish",
            "price": 10.99,
            "dish_type": 1,
            "cooks": [1, 2],
            "dish_photo": None,
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())


class CookSearchFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "last_name": "Doe",
        }
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "last_name": "",
        }
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class DishSearchFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "name": "Delicious Dish",
        }
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "name": "",
        }
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class DishTypeSearchFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            "name": "Main Course",
        }
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "name": "",
        }
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
