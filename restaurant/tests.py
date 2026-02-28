from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from .models import Menu, Booking


# ─────────────────────────────────────────
#  Model Tests
# ─────────────────────────────────────────

class MenuModelTest(TestCase):

    def setUp(self):
        self.menu_item = Menu.objects.create(
            title='Greek Salad',
            price=12.50,
            inventory=100,
        )

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.title, 'Greek Salad')
        self.assertEqual(float(self.menu_item.price), 12.50)
        self.assertEqual(self.menu_item.inventory, 100)

    def test_menu_str(self):
        expected = 'Greek Salad : 12.50'
        self.assertEqual(str(self.menu_item), expected)


class BookingModelTest(TestCase):

    def setUp(self):
        self.booking = Booking.objects.create(
            name='John Doe',
            no_of_guests=4,
            booking_date='2024-06-15 19:00:00',
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.name, 'John Doe')
        self.assertEqual(self.booking.no_of_guests, 4)

    def test_booking_str(self):
        self.assertEqual(str(self.booking), 'John Doe')


# ─────────────────────────────────────────
#  API Tests
# ─────────────────────────────────────────

class MenuAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        Menu.objects.create(title='Bruschetta', price=7.99, inventory=50)
        Menu.objects.create(title='Lemon Dessert', price=5.50, inventory=30)

    def test_get_all_menu_items(self):
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_create_menu_item(self):
        data = {'title': 'Grilled Fish', 'price': '18.00', 'inventory': 20}
        response = self.client.post('/api/menu/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Menu.objects.count(), 3)

    def test_get_single_menu_item(self):
        item = Menu.objects.first()
        response = self.client.get(f'/api/menu/{item.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], item.title)

    def test_update_menu_item(self):
        item = Menu.objects.first()
        data = {'title': 'Updated Item', 'price': '9.99', 'inventory': 15}
        response = self.client.put(f'/api/menu/{item.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        item.refresh_from_db()
        self.assertEqual(item.title, 'Updated Item')

    def test_delete_menu_item(self):
        item = Menu.objects.first()
        response = self.client.delete(f'/api/menu/{item.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Menu.objects.count(), 1)

    def test_unauthenticated_access(self):
        self.client.credentials()
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, 401)


class BookingAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser2', password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_booking(self):
        data = {
            'name': 'Alice Smith',
            'no_of_guests': 3,
            'booking_date': '2024-07-20T18:00:00Z',
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)

    def test_get_all_bookings(self):
        Booking.objects.create(name='Bob', no_of_guests=2, booking_date='2024-07-21T19:00:00Z')
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_booking(self):
        booking = Booking.objects.create(name='Carl', no_of_guests=5, booking_date='2024-07-22T20:00:00Z')
        data = {'name': 'Carl Updated', 'no_of_guests': 6, 'booking_date': '2024-07-22T20:00:00Z'}
        response = self.client.put(f'/api/bookings/{booking.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_booking(self):
        booking = Booking.objects.create(name='Dana', no_of_guests=2, booking_date='2024-07-23T19:00:00Z')
        response = self.client.delete(f'/api/bookings/{booking.id}/')
        self.assertEqual(response.status_code, 204)


class AuthAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'newuser@example.com',
        }
        response = self.client.post('/api/registration/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_duplicate_registration(self):
        User.objects.create_user(username='existing', password='pass123')
        data = {'username': 'existing', 'password': 'pass123'}
        response = self.client.post('/api/registration/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        User.objects.create_user(username='loginuser', password='loginpass')
        data = {'username': 'loginuser', 'password': 'loginpass'}
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_invalid_login(self):
        data = {'username': 'nobody', 'password': 'wrongpass'}
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, 400)


# ─────────────────────────────────────────
#  HTML View Tests
# ─────────────────────────────────────────

class HTMLViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)

    def test_menu_page(self):
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)

    def test_book_page(self):
        response = self.client.get('/book/')
        self.assertEqual(response.status_code, 200)
