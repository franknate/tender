from rest_framework import serializers
from core.models import Tender, Unit, BidRound, Bid, MARKET_CHOICES, DIRECTION_CHOICES

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'bid_round', 'price', 'amount', 'ours', 'unit']


class BidRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidRound
        fields = ['id', 'number', 'max_price_wkdy', 'max_price_wknd', 'tender']


class UnitSerializer(serializers.ModelSerializer):
    bids = BidSerializer(many=True, read_only=True)
    
    class Meta:
        model = Unit
        fields = ['id', 'fromdate', 'todate', 'tender', 'bids']


class TenderSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    bid_rounds = BidRoundSerializer(many=True, read_only=True)

    class Meta:
        model = Tender
        fields = ['id', 'date', 'market', 'direction', 'tender_round', 'bid_rounds', 'units']


class TenderOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = ['id', 'date', 'market', 'direction', 'tender_round']