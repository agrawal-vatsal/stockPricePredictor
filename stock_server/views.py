from datetime import datetime

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .files.integration import get_stock_price
from .models import Stock
# Create your views here.
from .utils.twitter_utils import get_polarity


class StockPrice(APIView):
    def get(self, request):
        stock_name = request.GET.get('name')
        date = datetime.date(datetime.now())
        try:
            stocks = Stock.objects.get(date=date, name=stock_name)
        except Stock.DoesNotExist:
            stocks = Stock(date=date, name=stock_name)
            data = get_stock_price(stock_name)
            polarity = get_polarity(stock_name)
            stocks.price = data[0][0]
            stocks.price += (stocks.price * polarity * 5) / 100
            stocks.polarity_positive = polarity > 0
            stocks.save()
        data = {
            'price': stocks.price,
            'polarity': stocks.polarity_positive
        }
        return Response(data=data, status=HTTP_200_OK)


class DeleteTableData(APIView):
    def get(self, request):
        date = datetime.date(datetime.now())
        stocks = Stock.objects.filter(date=date)
        stocks.delete()
        return Response(status=HTTP_200_OK)
