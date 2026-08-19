#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import Logger;


def clear_environ ():
    for k in [ 'TS' ]:
        if ( 'TS' in os.environ ):
            del ( os.environ [ 'TS' ] );


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger__create_log_tplTest ( unittest.TestCase ):
    def setUp ( self ):
        clear_environ ();

        
    def tearDown ( self ):
        clear_environ ();


    def test_base ( self ):
        l = Logger ();
        
        l._log_tpl = {
            'base': 'random-base'
        };

        ret = l._create_log_tpl ();
        
        self.assertEqual ( ret, 'random-base' );


    def test_ts_true ( self ):
        l = Logger ();
        
        l._log_tpl = {
            'base': 'random-base',
            'ts': 'random-ts'
        };

        os.environ [ 'TS' ] = 'true';

        ret = l._create_log_tpl ();
        
        self.assertEqual ( ret, 'random-ts random-base' );


    def test_ts_false ( self ):
        l = Logger ();
        
        l._log_tpl = {
            'base': 'random-base',
            'ts': 'random-ts'
        };

        os.environ [ 'TS' ] = 'false';

        ret = l._create_log_tpl ();
        
        self.assertEqual ( ret, 'random-base' );


if __name__ == '__main__':
    unittest.main ();
