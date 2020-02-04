from rest_framework import serializers

from bcg.payments.models import Ledger


class PaymentsChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        fields = ['amount', 'token']
