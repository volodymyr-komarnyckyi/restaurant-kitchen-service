from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.models import DishType, Dish


class DishListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish1 = Dish.objects.create(
            name="Dish 1",
            description="Description 1",
            price=9.99,
            dish_type=self.dish_type,
        )
        self.dish2 = Dish.objects.create(
            name="Dish 2",
            description="Description 2",
            price=12.50,
            dish_type=self.dish_type,
        )

    def test_dish_list_view(self):
        url = reverse("kitchen:dish-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dish 1")
        self.assertContains(response, "Dish 2")

    def test_dish_list_view_with_search(self):
        url = reverse("kitchen:dish-list")
        response = self.client.get(url, {"name": "Dish 1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dish 1")
        self.assertNotContains(response, "Dish 2")


class DishCreateViewTestCase(TestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_login(user)

    def test_dish_create_view(self):
        dish_type = DishType.objects.create(name="Main Course")
        url = reverse("kitchen:dish-create")

        form_data = {
            "name": "New Dish",
            "description": "A delicious new dish",
            "price": 12.99,
            "dish_type": dish_type.id,
        }

        response = self.client.post(url, form_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Dish.objects.filter(name="New Dish").exists())


class DishDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        self.dish_type = DishType.objects.create(name="Main Course")

        self.dish = Dish.objects.create(
            name="Test Dish",
            description="A delicious test dish",
            price=15.99,
            dish_type=self.dish_type,
        )

    def test_dish_detail_view(self):
        url = reverse("kitchen:dish-detail", args=[self.dish.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Dish")
        self.assertContains(response, "A delicious test dish")
        self.assertContains(response, "15.99")


class DishUpdateViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dish_type = DishType.objects.create(name="Main Course")
        cls.dish = Dish.objects.create(
            name="Test Dish",
            description="Test description",
            price=9.99,
            dish_type=cls.dish_type,
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_dish_update_view_get(self):
        self.client.force_login(self.user)
        url = reverse("kitchen:dish-update", args=[1])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class DishDeleteViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dish_type = DishType.objects.create(name="Main Course")
        cls.dish = Dish.objects.create(
            name="Test Dish",
            description="Test description",
            price=9.99,
            dish_type=cls.dish_type,
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_dish_delete_view_get(self):
        self.client.force_login(self.user)
        url = reverse(
            "kitchen:dish-delete", args=[self.dish.pk]
        )  # Use self.dish.pk here
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_confirm_delete.html")
        self.assertIn("object", response.context)
        self.assertEqual(response.context["object"], self.dish)

    def test_dish_delete_view_post(self):
        self.client.force_login(self.user)
        url = reverse(
            "kitchen:dish-delete", args=[self.dish.pk]
        )  # Use self.dish.pk here
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Dish.objects.filter(pk=self.dish.pk).exists())
        self.assertRedirects(response, reverse("kitchen:dish-list"))


class DishUpdateCookViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        dish_type = DishType.objects.create(name="dish_type")
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="Test description",
            price=9.99,
            dish_type=dish_type,
        )

        self.client = Client()

    def test_dish_update_cook_view_post_add_cook(self):
        self.client.force_login(self.user)
        url = reverse("kitchen:dish-update-cook", kwargs={"pk": self.dish.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse(
                "kitchen:dish-detail", kwargs={"pk": self.dish.pk}
            )
        )
        self.dish.refresh_from_db()
        self.assertTrue(self.user in self.dish.cooks.all())

    def test_dish_update_cook_view_post_remove_cook(self):
        self.dish.cooks.add(self.user)
        self.client.force_login(self.user)
        url = reverse("kitchen:dish-update-cook", kwargs={"pk": self.dish.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse(
                "kitchen:dish-detail", kwargs={"pk": self.dish.pk}
            )
        )
        self.dish.refresh_from_db()
        self.assertFalse(self.user in self.dish.cooks.all())
