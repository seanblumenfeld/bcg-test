from unittest.mock import patch

from django.test import TestCase, Client
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from bcg.payments.models import Ledger
from bcg.payments.services import PaymentsService
from bcg.payments.views import PaymentsServiceException


class PaymentApiTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_can_run_charge_card(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            data={
                'token': 'some-card-token',
                'amount': '123.45',
            }
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_ledger_object_created(self):
        self.client.post(
            path=reverse('payments_charge'),
            data={
                'token': 'some-card-token',
                'amount': '123.45',
            }
        )
        record = Ledger.objects.get(token='some-card-token')
        self.assertIsNotNone(record)

    def test_400_when_no_data_provided(self):
        response = self.client.post(reverse('payments_charge'))
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_400_when_token_not_provided(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            data={'amount': '123.45'},
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_400_when_amount_not_provided(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            data={'token': 'some-card-token'}
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_400_if_amount_not_a_decimal(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            data={'amount': 'bad-amount'}
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('bcg.payments.views.PaymentsService', autospec=PaymentsService)
    def test_400_when_payments_service_fails(self, payments_service_mock):
        payments_service_mock.charge_card.return_value = False
        response = self.client.post(
            path=reverse('payments_charge'),
            data={
                'token': 'some-card-token',
                'amount': '123.45',
            }
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertAlmostEqual(
            response.json()['detail'],
            PaymentsServiceException.default_detail
        )
