from decimal import Decimal

from django.test import TestCase

from bcg.payments.services import PaymentsService


class PaymentServiceTestCase(TestCase):

    def setUp(self):
        self.service = PaymentsService

    def test_can_charge_card(self):
        success = self.service.charge_card(
            token='fake-token',
            amount=Decimal('12.50'),
        )
        self.assertTrue(success)
