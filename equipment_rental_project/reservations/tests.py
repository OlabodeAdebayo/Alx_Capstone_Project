from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from equipment.models import Equipment
from .models import Reservation


class ReservationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='user1234')
        self.client.force_authenticate(user=self.user)

        self.equipment = Equipment.objects.create(
            name='Laptop',
            description='Dell Inspiron',
            is_available=True,
            rental_price=50.0
        )

        self.reservation_url = reverse('reservation-list')
        self.reservation_data = {
            'equipment': self.equipment.id,
            'start_date': '2025-10-15',
            'end_date': '2025-10-20'
        }

    def test_create_reservation(self):
        response = self.client.post(self.reservation_url, self.reservation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_edit_reservation(self):
        reservation = Reservation.objects.create(user=self.user, **self.reservation_data)
        url = reverse('reservation-detail', args=[reservation.id])
        updated_data = {'end_date': '2025-10-25'}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reservation.refresh_from_db()
        self.assertEqual(str(reservation.end_date), '2025-10-25')
        self.assertEqual(reservation.total_price, 300.0)  # 6 days * $50
        self.assertTrue(reservation.is_active)
    def test_cancel_reservation(self):
        reservation = Reservation.objects.create(user=self.user, **self.reservation_data)
        url = reverse('reservation-detail', args=[reservation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        reservation.refresh_from_db()
        self.assertFalse(reservation.is_active)
        self.assertEqual(reservation.total_price, 0)
        self.assertTrue(reservation.equipment.is_available)
