from django.test import TestCase, RequestFactory, Client
from .views import RateView
import json

class RateTests(TestCase):
    # initializes the view object
    def setUp(self):
        factory = RequestFactory()
        request = factory.get('/')
        self.view = self.setup_view(RateView(), request) 

    # returns the view object that is used to call the RateView methods 
    def setup_view(self,view, request, *args, **kwargs):
        view.request = request
        view.args = args
        view.kwargs = kwargs
        return view

    def test_is_invalid_date(self):
        self.assertEqual(self.view.is_invalid_date("1999-12-21"), False)
        self.assertEqual(self.view.is_invalid_date("2030-12-21"), True)
        self.assertEqual(self.view.is_invalid_date("1999/12/21"), True)
        self.assertEqual(self.view.is_invalid_date("1999-12"), True)
        self.assertEqual(self.view.is_invalid_date(""), True)

    def test_get_rate(self):
        expected_result = '{"amount":1.0,"base":"USD","date":"1999-12-21","rates":{"GBP":0.62237}}'
        self.assertEqual(self.view.get_rate("1999-12-21", "USD", "GBP").decode('ascii'), expected_result)     
