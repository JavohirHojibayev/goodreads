from unittest import TestCase

from django.urls import reverse
from users.models import CustomUser
from django.contrib.auth import get_user

class RegistrationTests(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "javohir",
                "first_name": "javohir",
                "last_name": "hojibayev",
                "email": "javohir@gmail.com",
                "password1": "javohir1108",
                "password2": "javohir1108"
            }
        )

        user = CustomUser.objects.get(username="javohir")

        self.assertEqual(user.first_name, "javohir")
        self.assertEqual(user.last_name, "hojibayev")
        self.assertEqual(user.email, "javohir@gmail.com")
        self.assertTrue(user.check_password("javohir1108"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "javohir",
                "email": "javohir@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required")

class LoginTests(TestCase):
    def test_successful_login(self):
        db_user = CustomUser.objects.create_user(username="javohir", email="javohir@gmail.com")
        db_user.set_password("javohir1108")
        db_user.save()

        self.client.post(
            reverse("users:login"),
            data={
                "username": "javohir",
                "password": "javohir1108"
            }
        )

        user = CustomUser.objects.get(username="javohir")

        self.assertTrue(user.is_authenticated)

    def test_logout(self):
        db_user = CustomUser.objects.create_user(username="javohir", email="javohir@gmail.com")
        db_user.set_password("javohir1108")
        db_user.save()

        self.client.login(username="javohir", password="javohir1108")

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile/")

    def test_profile_detail(self):
        user = CustomUser.objects.create_user(
            username="javohir", first_name="javohir", last_name="hojibayev", email="javohir@gmail.com")
        user.set_password("javohir1108")
        user.save()

        self.client.login(username="javohir", password="javohir1108")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create_user(
            username="javohir", first_name="javohir", last_name="hojibayev", email="javohir@gmail.com")
        user.set_password("javohir1108")
        user.save()

        self.client.login(username="javohir", password="javohir1108")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "javohir",
                "first_name": "javohir",
                "last_name": "hojibaye",
                "email": "javohir@gmail.com",
            })
        user.refresh_from_db()

        self.assertEqual(user.last_name, "hojibaye")
        self.assertEqual(user.email, "javohir@gmail.com")
        self.assertEqual(response.url, reverse("users:profile"))
