#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import Logger;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger__log_get_loggerTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.logger.logging.getLogger' ) as r_init:
            l = Logger ();

            ret = l._log_get_logger ();

            self.assertTrue ( isinstance ( ret, Mock ) );
            
            r_init.assert_called_once_with (
                None
            );

            
    def test_arg_name ( self ):
        with patch ( 'googlepostmasterapi.logger.logging.getLogger' ) as r_init:
            l = Logger ();

            ret = l._log_get_logger (
                name = 'random-name'
            );

            self.assertTrue ( isinstance ( ret, Mock ) );
            
            r_init.assert_called_once_with (
                'random-name'
            );


if __name__ == '__main__':
    unittest.main ();
