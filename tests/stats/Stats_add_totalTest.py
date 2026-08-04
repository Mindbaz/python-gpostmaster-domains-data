#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.stats import Stats;


class Stats_add_totalTest ( unittest.TestCase ):
    def test_calls ( self ):
        s = Stats ();
        s.data = { 'total': 123 };
        s.add_total ();
        
        self.assertEqual ( s.data [ 'total' ], 124 );
            
            
if __name__ == '__main__':
    unittest.main ();
