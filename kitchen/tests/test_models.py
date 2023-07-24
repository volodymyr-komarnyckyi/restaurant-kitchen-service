from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import DishType, Dish


class DishTypeModelTest(TestCase):
    def test_str_representation(self):
        dish_type = DishType.objects.create(name="Main Course")
        self.assertEqual(str(dish_type), "Main Course")


class CookModelTest(TestCase):
    def test_str_representation(self):
        cook = get_user_model().objects.create_user(
            username="chef123", first_name="John", last_name="Doe"
        )
        self.assertEqual(str(cook), "chef123 (John Doe)")


class DishModelTest(TestCase):
    def test_str_representation(self):
        dish_type = DishType.objects.create(name="Dessert")
        cook = get_user_model().objects.create_user(
            username="baker12", first_name="Alice", last_name="Smith"
        )
        dish = Dish.objects.create(
            name="Chocolate Cake",
            description="Delicious chocolate cake",
            price="25.00",
            dish_type=dish_type,
        )
        dish.cooks.add(cook)
        self.assertEqual(
            str(dish),
            "Chocolate Cake (price: 25.00, dish type: Dessert)"
        )
