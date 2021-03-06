# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client

from testlist.models import TestModel
from bootstrap_paginator.templatetags.paginator import urlencode_plus


class BootstrapPaginatorTestCase(TestCase):

    def setUp(self):
        for i in range(100):
            TestModel.objects.create()

    def test_paginator(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_unicode_get(self):
        response = Client().get('/?city=Montréal')
        self.assertEqual(response.status_code, 200)

    def test_unchanged(self):
        response = Client().get('/?text=smith')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('text=smith&page=2' in response.content)

    def test_urlencode_plus(self):
        self.assertTrue(
            'page=3' in urlencode_plus({'page': '2'}, page='3')
        )
        self.assertEqual(
            '?text=smith&page=3', urlencode_plus({'text': 'smith'}, page='3')
        )
