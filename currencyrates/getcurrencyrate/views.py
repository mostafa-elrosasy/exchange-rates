from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Rate
from .serializers import RateSerializer
from django.http import HttpResponse
import requests
import ast
import json
from datetime import datetime


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

    def get(self, request):
        date = request.data["date"]
        source = request.data["from"]
        destination = request.data["to"]
        rate = Rate.objects.filter(source_currency=source, destination_currency=destination, date=date).first()
        if rate == None:   
            rate_request = self.get_rate(date, source, destination)
            rate = self.save_rate(rate_request)
        serializer = RateSerializer(rate)
        return Response(serializer.data)
