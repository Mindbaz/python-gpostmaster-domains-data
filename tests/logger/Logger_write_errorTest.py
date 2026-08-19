#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import Logger;


class RMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'RMock : __init__' );
        pass;

    def error ( self, *args, **kargs ):
        print ( 'RMock : error' );
        pass;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger_write_errorTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.logger.Logger._get_current_class_name' ) as get_current_class_name:
             with patch ( 'tests.logger.Logger_write_errorTest.RMock.error' ) as print_error:
                 get_current_class_name.return_value = 'random-class-name';
                 
                 l = Logger ();
                 l._logger = RMock ();
             
                 l.write_error (
                     logs = [
                         'random-log-1',
                         'random-log-2',
                         'random-log-3'
                     ]
                 );
             
                 self.assertEqual ( print_error.call_count, 3 );
                 print_error.assert_any_call ( 'random-log-1', extra = { 'class_name': 'random-class-name' } );
                 print_error.assert_any_call ( 'random-log-2', extra = { 'class_name': 'random-class-name' } );
                 print_error.assert_any_call ( 'random-log-3', extra = { 'class_name': 'random-class-name' } );


if __name__ == '__main__':
    unittest.main ();
