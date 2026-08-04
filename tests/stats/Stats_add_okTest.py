#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.stats import Stats;


class Stats_add_okTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.stats.Stats.add_total' ) as add_total:
            s = Stats ();
            s.data = { 'ok': 456 };
            s.add_ok ();
            self.assertEqual ( s.data [ 'ok' ], 457 );
            add_total.assert_called_once_with ();
            
            
if __name__ == '__main__':
    unittest.main ();
