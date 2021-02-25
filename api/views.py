from .models import Tender, Unit
from .serializers import TenderOnlySerializer, TenderSerializer
from .functions import save_to_db
from rest_framework import viewsets, status
from rest_framework.response import Response


class TenderViewSet(viewsets.ModelViewSet):
    queryset = Tender.objects.all().order_by('-date')
    serializer_class = TenderSerializer
    ordering = ['date']

    def list(self, request):
        queryset = Tender.objects.all()
        serializer = TenderOnlySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if not save_to_db(request.data):
            return Response({"Success": "Unvalid column names"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({"Success": "Uploaded succesfully"}, status=status.HTTP_202_ACCEPTED)

    def update(self, request, *args, **kwargs):
        if not save_to_db(request.data):
            return Response({"Success": "Unvalid column names"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({"Success": "Uploaded succesfully"}, status=status.HTTP_202_ACCEPTED)