#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import Logger;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger__init_logger_formatTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.logger.Logger._create_log_tpl' ) as create_tpl:
            with patch ( 'googlepostmasterapi.logger.logging.Formatter' ) as formatter_init:
                create_tpl.return_value = 'random-tpl';

                l = Logger ();

                ret = l._init_logger_format ();

                self.assertTrue ( isinstance ( ret, Mock ) );

                create_tpl.assert_called_once_with ();
                formatter_init.assert_called_once_with (
                    'random-tpl'
                );


if __name__ == '__main__':
    unittest.main ();
