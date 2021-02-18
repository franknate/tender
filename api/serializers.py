from rest_framework import serializers
from api.models import Tender, Unit, Bid, MARKET_CHOICES, DIRECTION_CHOICES

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'bid_round', 'price', 'amount', 'ours', 'unit']


class UnitSerializer(serializers.ModelSerializer):
    bids = BidSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ['id', 'fromdate', 'todate', 'tender', 'bids']


class TenderSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Tender
        fields = ['id', 'date', 'market', 'direction', 'tender_round', 'units']


class TenderOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = ['id', 'date', 'market', 'direction', 'tender_round']