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
    
    def addFilter ( self, *args, **kargs ):
        print ( 'RMock : addFilter' );
        pass;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger__log_add_filterTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.logger.LoggingFilter' ) as r_init:
            with patch ( 'tests.logger.Logger__log_add_filterTest.RMock.addFilter' ) as addFilter:
                r_init.side_effect = RMock;
                l = Logger ();

                l._log_add_filter (
                    logger = RMock (),
                    level = 123
                );

                r_init.assert_called_once_with (
                    level = 123
                );

                self.assertEqual ( addFilter.call_count, 1 );
                for call in addFilter.call_args_list:
                    args, kwargs = call;
                    self.assertTrue ( isinstance ( args [ 0 ], RMock ) );


if __name__ == '__main__':
    unittest.main ();
