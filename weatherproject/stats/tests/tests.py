# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TestStatsView(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_historical_records(self):
        res = self.client.get(reverse('historical_record'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_statistic(self):
        res = self.client.get(reverse('statistic'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
