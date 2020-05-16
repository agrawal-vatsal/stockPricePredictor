from datetime import datetime

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from .files.integration import get_stock_price
from .models import Stock


# Create your views here.

class StockPrice(APIView):
    def get(self, request):
        stock_name = request.GET.get('name')
        date = datetime.date(datetime.now())
        try:
            stocks = Stock.objects.get(date=date, name=stock_name)
            return Response(data=stocks.price, status=HTTP_200_OK)
        except Stock.DoesNotExist:
            stocks = Stock(date=date, name=stock_name)
            data = get_stock_price(stock_name)
            stocks.price = data[0][0]
            stocks.save()
        return Response(data=data[0][0], status=HTTP_200_OK)
