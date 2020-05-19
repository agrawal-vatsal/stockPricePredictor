from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from stock_server.models import Stock


class StockDataSerializer(ModelSerializer):
    polarity = serializers.BooleanField(source='polarity_positive')

    class Meta:
        model = Stock
        fields = ('price', 'polarity')
