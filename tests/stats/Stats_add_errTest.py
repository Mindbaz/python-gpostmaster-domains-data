#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.stats import Stats;


class Stats_add_errTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.stats.Stats.add_total' ) as add_total:
            s = Stats ();
            s.data = { 'err': 789 };
            s.add_err ();
            self.assertEqual ( s.data [ 'err' ], 790 );
            add_total.assert_called_once_with ();
            

if __name__ == '__main__':
    unittest.main ();
