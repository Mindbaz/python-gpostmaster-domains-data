#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import Logger;
from logging import WARNING;
import sys;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger__init_logger_stderrTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.logger.logging.StreamHandler' ) as r_init:
            with patch ( 'googlepostmasterapi.logger.Logger._log_set_format' ) as log_set_format:
                with patch ( 'googlepostmasterapi.logger.Logger._log_set_level' ) as log_set_level:
                    r_init.return_value = 'random-sh';
                    
                    l = Logger ();

                    ret = l._init_logger_stderr (
                        log_format = 'random-log-format'
                    );

                    self.assertEqual ( ret, 'random-sh' );

                    r_init.assert_called_once_with (
                        sys.stderr
                    );
                    log_set_format.assert_called_once_with (
                        logger = 'random-sh',
                        log_format = 'random-log-format'
                    );
                    log_set_level.assert_called_once_with (
                        logger = 'random-sh',
                        level = WARNING
                    );


if __name__ == '__main__':
    unittest.main ();
