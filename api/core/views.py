from .models import Tender, Unit
from .serializers import TenderOnlySerializer, TenderSerializer
from .functions import create_new_tender, update_tender, make_bid, initial_bids, printException
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse
from django.core.files import File


class TenderViewSet(viewsets.ModelViewSet):
    queryset = Tender.objects.all().order_by('-datestr')
    serializer_class = TenderSerializer
    ordering = ['datestr']

    def list(self, request):
        queryset = Tender.objects.all()
        serializer = TenderOnlySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            tender_id = create_new_tender(request.data)
            return Response({"message": "Uploaded succesfully", "id": tender_id}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            printException()
            return Response({"message": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
    def update(self, request, *args, **kwargs):
        try:
            update_tender(request.data)
            return Response({"message": "Uploaded succesfully"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            printException()
            return Response({"message": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class BidView(APIView):
    def get(self, request, tender_id, format=None):
        try:
            return Response(initial_bids(tender_id))
        except Exception as e:
            printException()
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, tender_id, format=None):
        try:
            filepath = make_bid(request.data, tender_id)
            bid_file = open(filepath, 'rb')
            return FileResponse(File(bid_file), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e:
            printException()
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
