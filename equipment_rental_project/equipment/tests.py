from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Equipment


class EquipmentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin123')
        self.client.force_authenticate(user=self.user)
        self.equipment_url = reverse('equipment-list')
        self.equipment_data = {
            'name': 'Camera',
            'description': 'DSLR Camera',
            'is_available': True,
            'rental_price': 25.0
        }

    def test_create_equipment(self):
        response = self.client.post(self.equipment_url, self.equipment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Equipment.objects.count(), 1)

    def test_list_equipment(self):
        Equipment.objects.create(**self.equipment_data)
        response = self.client.get(self.equipment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
