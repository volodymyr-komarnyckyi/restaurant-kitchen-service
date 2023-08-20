from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import DishType


class DishTypeListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="testuser", password="testpassword"
        )
        self.client.login(email="testuser", password="testpassword")
        self.dish_type = DishType.objects.create(name="Main Course")

    def test_dish_type_list_view(self):
        url = reverse("kitchen:dish-type-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Main Course")

    def test_dish_type_list_view_with_search(self):
        url = reverse("kitchen:dish-type-list")
        response = self.client.get(url, {"name": "Main"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Main Course")


class DishTypeCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="testuser", password="testpassword"
        )
        self.client.login(email="testuser", password="testpassword")

    def test_dish_type_create_view(self):
        url = reverse("kitchen:dish-type-create")
        response = self.client.post(url, {"name": "Main Course"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DishType.objects.count(), 1)
        self.assertEqual(DishType.objects.first().name, "Main Course")


class DishTypeDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser", password="testpassword"
        )
        self.client.login(email="testuser", password="testpassword")

        self.dish_type = DishType.objects.create(name="Salad")

    def test_dish_type_delete_view(self):
        url = reverse("kitchen:dish-type-delete", args=[self.dish_type.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(DishType.objects.filter(name="Salad").exists())


class DishTypeUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser", password="testpassword"
        )
        self.client.login(email="testuser", password="testpassword")

        self.dish_type = DishType.objects.create(name="Salad")

    def test_dish_type_update_view_get(self):
        url = reverse("kitchen:dish-type-update", args=[self.dish_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Salad")

    def test_dish_type_update_view_post(self):
        url = reverse("kitchen:dish-type-update", args=[self.dish_type.id])
        form_data = {
            "name": "New Dish Type Name",
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)

        self.dish_type.refresh_from_db()
        self.assertEqual(self.dish_type.name, "New Dish Type Name")
