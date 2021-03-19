from .models import Tender, Unit
from .serializers import TenderOnlySerializer, TenderSerializer
from .functions import create_new_tender, update_tender, crate_bid_file
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.core.files import File


class TenderViewSet(viewsets.ModelViewSet):
    queryset = Tender.objects.all().order_by('-date')
    serializer_class = TenderSerializer
    ordering = ['date']

    def list(self, request):
        queryset = Tender.objects.all()
        serializer = TenderOnlySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            create_new_tender(request.data)
            return Response({"message": "Uploaded succesfully"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print("Exception:", e)
            return Response({"message": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            

    def update(self, request, *args, **kwargs):
        try:
            update_tender(request.data)
            return Response({"message": "Uploaded succesfully"}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            print("Exception:", e)
            return Response({"message": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['POST'])
def make_bid(request):
    try:
        filepath = crate_bid_file(request.data)
        bid_file = open(filepath, 'rb')
        return HttpResponse(File(bid_file), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        print("Exception:", e)
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)