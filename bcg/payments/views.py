from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from bcg.payments.models import Ledger
from bcg.payments.serializers import PaymentsChargeSerializer
from bcg.payments.services import PaymentsService


class PaymentsServiceException(APIException):
    status_code = 400
    default_detail = 'External Payment Service Error.'
    default_code = 'external_payment_service_error'


class PaymentsChargeAPIView(GenericAPIView):
    """Api to process a payment charge."""
    queryset = Ledger.objects.all()
    serializer_class = PaymentsChargeSerializer
    permission_classes = []  # TODO

    def post(self, request, *args, **kwargs):
        # Validate request data (return 400 if bad)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # send to external payments service
        success = PaymentsService.charge_card(**serializer.validated_data)

        if not success:
            raise PaymentsServiceException()

        # Create record in our ledger if external payment successful
        serializer.save()

        return Response(serializer.validated_data)
