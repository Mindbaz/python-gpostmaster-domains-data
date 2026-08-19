#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.base import Base;


class Base_extract_stat_valueTest ( unittest.TestCase ):
    def test_no_value ( self ):
        b = Base ();
        
        ret = b.extract_stat_value ( value = None );
        self.assertEqual ( ret, None );


    def test_double_value ( self ):
        b = Base ();
        
        ret = b.extract_stat_value (
            value = {
                'doubleValue': 0.1234
            }
        );
        self.assertEqual ( ret, 0.1234 );


    def test_float_value ( self ):
        b = Base ();
        
        ret = b.extract_stat_value (
            value = {
                'floatValue': 0.4567
            }
        );
        self.assertEqual ( ret, 0.4567 );


    def test_int_value ( self ):
        b = Base ();
        
        ret = b.extract_stat_value (
            value = {
                'intValue': '789'
            }
        );
        self.assertEqual ( ret, 789 );


    def test_string_value ( self ):
        b = Base ();
        
        ret = b.extract_stat_value (
            value = {
                'stringValue': 'random-value'
            }
        );
        self.assertEqual ( ret, 'random-value' );


    def test_string_list ( self ):
        b = Base ();
        
        ret = b.extract_stat_value (
            value = {
                'stringList': {
                    'values': [
                        'random-value-1',
                        'random-value-2'
                    ]
                }
            }
        );
        self.assertEqual ( ret, [
            'random-value-1',
            'random-value-2'
        ] );


    def test_empty_value ( self ):
        b = Base ();
        
        ret = b.extract_stat_value ( value = {} );
        self.assertEqual ( ret, None );
                        
            
if __name__ == '__main__':
    unittest.main ();
