from django.test import TestCase
from django.urls import reverse
from books.models import Book
from users.models import CustomUser


class BookTestCase(TestCase):
    def test_no_book(self):
        response = self.client.get(reverse("books:list"))
        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="113122")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="143123")

        response = self.client.get(reverse("books:list") + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")
        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="description1", isbn="123121")
        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description="Description1", isbn="123121")
        book2 = Book.objects.create(title="Guide", description="Description2", isbn="113122")
        book3 = Book.objects.create(title="Shoe Dog", description="Description3", isbn="143123")

        response = self.client.get(reverse("books:list") + "?search=sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?search=Guide")
        self.assertNotContains(response, book1.title)
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?search=Shoe+Dog")
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertContains(response, book3.title)


class BookReviewTests(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123123")
        user = CustomUser.objects.create(
            username='javohir',
            first_name='hojibayev',
            last_name='javohir',
            email='javohir@gmail.com'
        )
        user.set_password("javohir")
        user.save()

        self.client.login(username="javohir", password="javohir")

        self.client.post(reverse("books:review", kwargs={"id": book.id}), data={
            "stars_given": 3,
            "comment": "nice book"
        })

        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)

