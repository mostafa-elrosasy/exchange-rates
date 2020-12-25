from .models import Rate
from rest_framework import serializers


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ['source_currency', 'destination_currency', 'date', 'rate']
