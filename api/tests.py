from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser

class BookReviewAPITests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='javohir', first_name='javohir')
        self.user.set_password('javohir1108')
        self.user.save()
        self.client.login(username='javohir', password='jaovhri1108')

    def test_book_review_detail(self):
        book = Book.objects.create(title='Book1', description='Description', isbn='1231234')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good book")

        response = self.client.get(reverse('api:review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'],5)
        self.assertEqual(response.data['comment'], "very good book")
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Book1' )
        self.assertEqual(response.data['book']['description'], 'Description')
        self.assertEqual(response.data['book']['isbn'], '1231234')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], 'javohir')
        self.assertEqual(response.data['user']['username'], 'javohir')

    def test_book_review_list(self):
        user_two = CustomUser.objects.create_user(username='somebody', first_name='somebody')

        book = Book.objects.create(title='Book1', description='Description', isbn='1231234')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="very good book")
        br_two = BookReview.objects.create(book=book, user=user_two, stars_given=3, comment="Not good book")

        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['id'], br.id)
        self.assertEqual(response.data[1]['id'], br_two.id)
