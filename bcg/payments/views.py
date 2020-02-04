from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from bcg.payments.serializers import PaymentsChargeSerializer
from bcg.payments.services import PaymentsService


class PaymentsServiceException(APIException):
    status_code = 400
    default_detail = 'External Payment Service Error.'
    default_code = 'external_payment_service_error'


class PaymentsChargeAPIView(GenericAPIView):
    """Api to process a payment charge."""
    # queryset = Ledger.objects.all()
    serializer_class = PaymentsChargeSerializer
    permission_classes = []  # TODO

    def post(self, request, *args, **kwargs):
        request_data = {'user_id': request.headers.get('X-REQUEST-ID')}
        request_data.update(request.data)
        serializer = self.get_serializer(data=request_data)

        # Validate request data (return 400 if bad)
        serializer.is_valid(raise_exception=True)

        # send to external payments service
        points_balance = PaymentsService.charge_card(**serializer.validated_data)

        if not points_balance:
            raise PaymentsServiceException()

        return Response(
            {'points_balance': points_balance}
        )
