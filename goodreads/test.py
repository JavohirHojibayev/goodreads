from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview
from users.models import CustomUser

class HomePageTest(TestCase):
    def test_paginated_list(self):
        books = Book.objects.create(title="Book 1", description="Description 1", isbn="123123")
        user = CustomUser.objects.create(
            username="javohir", first_name="javohir", last_name="hojibayev", email="javohir@gmial.com"
        )
        user.set_password("javohir")
        user.save()
        review1 = BookReview.objects.create(book=books, user=user, stars_given=3, comment="good")
        review2 = BookReview.objects.create(book=books, user=user, stars_given=4, comment="very good")
        review3 = BookReview.objects.create(book=books, user=user, stars_given=2, comment="nice")

        response = self.client.get(reverse('home_page') + "?page_size=2")

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
