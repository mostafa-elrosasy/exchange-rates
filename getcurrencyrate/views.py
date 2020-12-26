from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Rate
from .serializers import RateSerializer
import requests
import ast
from datetime import datetime, date as dt
from rest_framework import status

class RateView(APIView):
    # constructs the url used to get the exchange rate from frankfurter
    # and returns the response body
    def get_rate(self, date, source, destination):
        url = "https://api.frankfurter.app/{}?from={}&to={}".format(date, source, destination)
        rate = requests.get(url)
        return rate.content

    # constructs a new rate object from frankfurter response body, 
    # saves the object in the database, and returns the object 
    def save_rate(self, rate_object):
        rate_object = ast.literal_eval(rate_object.decode("UTF-8"))
        date = rate_object["date"]
        source = rate_object["base"]
        destination = [*rate_object["rates"]][0]
        rate = rate_object["rates"][destination]
        # for some dates frankfurter returns other dates (for 2009-01-25 the date of the returned rate is 2009-01-23)
        # so this line checks if the returned rate is already in the database to prevent duplicates
        new_rate = Rate.objects.filter(source_currency=source, destination_currency=destination, date=date).first()
        if new_rate == None:
            new_rate = Rate(source_currency = source, destination_currency = destination, date = date, rate = rate)
            new_rate.save()
        return new_rate

    # if the date is in the future or the date format is not yyyy-mm-dd (invalid date)
    # the function returns true
    def is_invalid_date(self, date):
        try:
            if datetime.strptime(date, '%Y-%m-%d') > datetime.today():
                return True
            else:
                return False
        except ValueError:
            return True

    # serves the get request
    def get(self, request):
        try:
            date = request.data["date"]
            # used upper to accept currencies in different letter cases (USD and usd are treated the same)
            source = request.data["from"].upper()
            destination = request.data["to"].upper()
            if self.is_invalid_date(date):
                return Response({"message":"Invalid date"}, status=status.HTTP_400_BAD_REQUEST)
            rate = Rate.objects.filter(source_currency=source, destination_currency=destination, date=date).first()
            # if the requested rate isn't in the database, it's got from frankfurter and saved in the database
            if rate == None:
                rate_request = self.get_rate(date, source, destination)
                rate = self.save_rate(rate_request)
            serializer = RateSerializer(rate)
            return Response(serializer.data)
        # when a field in missing, a KeyError is raised
        except KeyError as e:
            return Response({"message":str(e)+" field is missing"}, status=status.HTTP_400_BAD_REQUEST)
        # raised with wrong date format (2015-3-29 instead of 2015-03-29) 
        except ValueError:
            return Response({"message":"make sure the date format is yyyy-mm-dd"}, status=status.HTTP_400_BAD_REQUEST)
        # when currency field has wrong data (like USDD) a syntax error is raised
        except SyntaxError:
            return Response({"message":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        # except:
        #     return Response({"message":"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

