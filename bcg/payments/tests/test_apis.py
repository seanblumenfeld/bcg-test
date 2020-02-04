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

    def test_400_when_no_request_id_in_header(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_400_when_no_data_provided(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            HTTP_X_REQUEST_ID='abcd'
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_400_when_token_not_provided(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data={'amount': '123.45'},
            HTTP_X_REQUEST_ID='abcd'
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_400_when_amount_not_provided(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data={'token': 'some-card-token'},
            HTTP_X_REQUEST_ID='abcd'
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_400_if_amount_not_a_decimal(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data={'amount': 'bad-amount'},
            HTTP_X_REQUEST_ID='abcd'
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @patch('bcg.payments.views.PaymentsService', autospec=PaymentsService)
    def test_400_when_payments_service_fails(self, payments_service_mock):
        payments_service_mock.charge_card.return_value = False
        response = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data={
                'token': 'some-card-token',
                'amount': '123.45',
            },
            HTTP_X_REQUEST_ID='abcd'
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertAlmostEqual(
            response.json()['detail'],
            PaymentsServiceException.default_detail
        )

    def test_can_run_charge_card(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data={
                'token': 'some-card-token',
                'amount': '123.45',
            },
            HTTP_X_REQUEST_ID='abcd'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_ledger_object_created(self):
        self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data={
                'token': 'some-card-token',
                'amount': '123.45',
            },
            HTTP_X_REQUEST_ID='abcd'
        )
        record = Ledger.objects.get(token='some-card-token')
        self.assertIsNotNone(record)

    def test_loyalty_points_for_new_user(self):
        response = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data={
                'token': 'some-card-token',
                'amount': '200.00',
            },
            HTTP_X_REQUEST_ID='abcd'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()['points_balance'], 4)

    def test_loyalty_points_for_existing_user(self):
        charge_data = {
            'token': 'some-card-token',
            'amount': '200.00',
        }
        self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data=charge_data,
            HTTP_X_REQUEST_ID='abcd'
        )
        response = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data=charge_data,
            HTTP_X_REQUEST_ID='abcd'
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json()['points_balance'], 8)

    def test_loyalty_points_for_two_users(self):
        charge_data = {
            'token': 'some-card-token',
            'amount': '200.00',
        }
        response1 = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data=charge_data,
            HTTP_X_REQUEST_ID='xyz'
        )
        response2 = self.client.post(
            path=reverse('payments_charge'),
            content_type='application/json',
            data=charge_data,
            HTTP_X_REQUEST_ID='abc'
        )
        self.assertEqual(response1.json()['points_balance'], 4)
        self.assertEqual(response2.json()['points_balance'], 4)
