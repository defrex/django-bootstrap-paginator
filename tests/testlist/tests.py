
from django.test import TestCase, Client

from testlist.models import TestModel


class BootstrapPaginatorTestCase(TestCase):

    def setUp(self):
        for i in range(100):
            TestModel.objects.create()

    def test_paginator(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)
