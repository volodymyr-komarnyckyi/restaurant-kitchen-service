from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from kitchen.forms import CookCreationForm
from kitchen.models import Cook


class CookListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_login(self.user)
        self.cook1 = get_user_model().objects.create_user(
            username="cook1",
            first_name="John",
            last_name="Doe",
            email="john@gmail.com"
        )
        self.cook2 = get_user_model().objects.create_user(
            username="cook2",
            first_name="Alice",
            last_name="Smith",
            email="alice@gmail.com"
        )

    def test_cook_list_view(self):
        url = reverse("kitchen:cook-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "John")
        self.assertContains(response, "Doe")
        self.assertContains(response, "None")

    def test_cook_list_view_with_search(self):
        url = reverse("kitchen:cook-list")
        response = self.client.get(url, {"last_name": "Doe"})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "John")
        self.assertContains(response, "Doe")
        self.assertContains(response, "None")
        self.assertNotContains(response, "Alice")
        self.assertNotContains(response, "Smith")


class CookDetailViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cook = get_user_model().objects.create(
            username="testcook",
            first_name="John",
            last_name="Doe",
            email="test@example.com",
            years_of_experience=5,
        )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_cook_detail_view(self):
        self.client.force_login(self.user)

        url = reverse(
            "kitchen:cook-detail", args=[self.cook.pk]
        )  # Use self.cook.pk here

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "kitchen/cook_detail.html")

        self.assertIn("object", response.context)
        self.assertEqual(response.context["object"], self.cook)


class CookCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_cook_create_view_get(self):
        self.client.force_login(self.user)

        url = reverse("kitchen:cook-create")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "kitchen/cook_form.html")

        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], CookCreationForm)

    def test_cook_create_view_post(self):
        self.client.force_login(self.user)

        url = reverse("kitchen:cook-create")

        data = {
            "username": "newcook",
            "first_name": "New",
            "last_name": "Cook",
            "email": "newcook@example.com",
            "years_of_experience": 2,
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Cook.objects.filter(username="newcook").exists())

        self.assertRedirects(response, reverse("kitchen:cook-list"))


class CookUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.cook = Cook.objects.create(
            username="cook1",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            years_of_experience=5,
        )
        self.url = reverse("kitchen:cook-update", kwargs={"pk": self.cook.pk})
        self.client.force_login(self.user)

    def test_cook_update_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Update Cook")
        self.assertContains(response, 'value="John"')
        self.assertContains(response, 'value="Doe"')

    def test_cook_update_view_post(self):
        data = {
            "username": "updated_cook",
            "first_name": "Updated",
            "last_name": "Cook",
            "email": "updated_cook@example.com",
            "years_of_experience": 7,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.cook.refresh_from_db()
        self.assertEqual(self.cook.username, "updated_cook")
        self.assertEqual(self.cook.first_name, "Updated")
        self.assertEqual(self.cook.years_of_experience, 7)
        self.assertRedirects(response, reverse("kitchen:cook-list"))


class CookDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.cook = Cook.objects.create(
            username="cook1",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            years_of_experience=5,
        )
        self.url = reverse("kitchen:cook-delete", kwargs={"pk": self.cook.pk})
        self.client.force_login(self.user)

    def test_cook_delete_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete Cook")
        self.assertContains(response, "John Doe")

    def test_cook_delete_view_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Cook.objects.filter(pk=self.cook.pk).exists())
        self.assertRedirects(response, reverse("kitchen:cook-list"))
