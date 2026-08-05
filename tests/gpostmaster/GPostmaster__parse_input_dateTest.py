#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__parse_input_dateTest ( unittest.TestCase ):
    def test_calls ( self ):
        g = GPostmaster (
            token = 'random-token'
        );

        ret = g._parse_input_date (
            input_date = '20261101'
        );

        self.assertEqual ( ret, { 'year': 2026, 'month': 11, 'day': 1 } );


if __name__ == '__main__':
    unittest.main ();
