from decimal import Decimal

from django.test import TestCase

from bcg.payments.models import Balances, Ledger
from bcg.payments.services import PaymentsService, BalancesService, LedgerService


class PaymentServiceTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.service = PaymentsService

    def test_charge_card_creates_ledger_and_balance_records(self):
        self.service.charge_card(
            user_id='fake-user-id',
            token='fake-token',
            amount=Decimal('200'),
        )
        self.assertEqual(Ledger.objects.count(), 1)
        self.assertEqual(Balances.objects.count(), 1)


class BalancesServiceTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.service = BalancesService

    def test_create_new_user_balance(self):
        balance = self.service.update_user_balance(
            user_id='fake-user-id',
            amount=Decimal('200'),
        )
        self.assertTrue(balance.points_balance, 4)

    def test_update_existing_user_balance(self):
        user_id = 'fake-user-id'
        balance = Balances(
            user_id=user_id,
            points_balance=Decimal('10')
        )
        balance.save()
        new_balance = self.service.update_user_balance(
            user_id=user_id,
            amount=Decimal('200'),
        )
        self.assertTrue(new_balance.points_balance, 14)


class LedgerServiceTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.service = LedgerService

    def test_create_new_ledger_record(self):
        self.service.create_ledger_record(
            user_id='fake-user-id',
            token='fake-token',
            amount=Decimal('200'),
        )
        self.assertTrue(Ledger.objects.get(user_id='fake-user-id'))
