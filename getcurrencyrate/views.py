from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Rate
from .serializers import RateSerializer
import requests
import ast
from datetime import datetime, date as dt
from rest_framework import status



class RateView(APIView):

    def get_rate(self, date, source, destination):
        url = "https://api.frankfurter.app/{}?from={}&to={}".format(date, source, destination)
        rate = requests.get(url)
        return(rate.content)

    def save_rate(self, rate_object):
        rate_object = ast.literal_eval(rate_object.decode("UTF-8"))
        date = rate_object["date"]
        source = rate_object["base"]
        destination = [*rate_object["rates"]][0]
        rate = rate_object["rates"][destination]
        new_rate = Rate(source_currency = source, destination_currency = destination, date = date, rate = rate)
        new_rate.save()
        print("saved to database")
        return new_rate

    def is_invalid_date(self, date):
        try:
            if datetime.strptime(date, '%Y-%m-%d') > datetime.today():
                return True
            else:
                return False
        except ValueError:
            return True

    def get(self, request):
        try:
            date = request.data["date"]
            source = request.data["from"].upper()
            destination = request.data["to"].upper()
            if self.is_invalid_date(date):
                return Response({"message":"Invalid date"}, status=status.HTTP_400_BAD_REQUEST)
            rate = Rate.objects.filter(source_currency=source, destination_currency=destination, date=date).first()
            if rate == None:
                rate_request = self.get_rate(date, source, destination)
                rate = self.save_rate(rate_request)
            serializer = RateSerializer(rate)
            return Response(serializer.data)
        except KeyError as e:
            return Response({"message":str(e)+" field is missing"}, status=status.HTTP_400_BAD_REQUEST)
        except (SyntaxError):
            return Response({"message":"Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

