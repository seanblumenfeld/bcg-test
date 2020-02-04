from decimal import Decimal

from bcg.payments.models import Ledger, Balances


class LedgerService:

    @staticmethod
    def create_ledger_record(user_id: str, token: str, amount: Decimal):
        record = Ledger(user_id=user_id, token=token, amount=amount)
        record.save()


class BalancesService:
    cashback_rate = Decimal('0.02')

    @classmethod
    def update_user_balance(cls, user_id: str, amount: Decimal):
        user_balance, created = Balances.objects.get_or_create(user_id=user_id)
        points_to_add = int(amount * cls.cashback_rate)
        user_balance.points_balance += points_to_add
        user_balance.save()
        return user_balance


class PaymentsService:

    @staticmethod
    def charge_card(user_id: str, token: str, amount: Decimal):
        """
        TODO: Adapter to deal with our external payments service.

        returns:
            int:New points balance for user
        """
        # The code here would need to be implemented to interact with our
        # payments service/provider, eg:
        # requests.post(..., data={})
        balance = BalancesService.update_user_balance(user_id=user_id, amount=amount)
        LedgerService.create_ledger_record(user_id=user_id, token=token, amount=amount)
        return balance.points_balance
