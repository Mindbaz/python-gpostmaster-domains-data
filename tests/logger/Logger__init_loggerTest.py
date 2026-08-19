#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import Logger;
from logging import DEBUG;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger__init_loggerTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.logger.Logger._init_logger_format' ) as init_logger_format:
            with patch ( 'googlepostmasterapi.logger.Logger._log_get_logger' ) as log_get_logger:
                with patch ( 'googlepostmasterapi.logger.Logger._init_logger_stdout' ) as init_logger_stdout:
                    with patch ( 'googlepostmasterapi.logger.Logger._init_logger_stderr' ) as init_logger_stderr:
                        with patch ( 'googlepostmasterapi.logger.Logger._log_add_handler' ) as log_add_handler:
                            with patch ( 'googlepostmasterapi.logger.Logger._log_set_level' ) as log_set_level:
                                init_logger_format.return_value = 'random-format';
                                root_logger_mock = Mock (
                                    handlers = []
                                );
                                log_get_logger.side_effect = [
                                    root_logger_mock,
                                    'random-logger'
                                ];
                                init_logger_stdout.return_value = 'random-logger-stdout';
                                init_logger_stderr.return_value = 'random-logger-stderr';
                                
                                l = Logger ();

                                ret = l._init_logger ();

                                self.assertEqual ( l._logger, 'random-logger' );

                                init_logger_format.assert_called_once_with ();
                                self.assertEqual ( log_get_logger.call_count, 2 );
                                log_get_logger.assert_any_call ();
                                log_get_logger.assert_any_call (
                                    name = 'Logger'
                                );
                                init_logger_stdout.assert_called_once_with (
                                    log_format = 'random-format'
                                );
                                init_logger_stderr.assert_called_once_with (
                                    log_format = 'random-format'
                                );
                                self.assertEqual ( log_add_handler.call_count, 2 );
                                log_add_handler.assert_any_call (
                                    logger = root_logger_mock,
                                    handler = 'random-logger-stdout'
                                );
                                log_add_handler.assert_any_call (
                                    logger = root_logger_mock,
                                    handler = 'random-logger-stderr'
                                );
                                log_set_level.assert_called_once_with (
                                    logger = 'random-logger',
                                    level = DEBUG
                                );

                                
    def test_root_logger_handlers_already_set ( self ):
        with patch ( 'googlepostmasterapi.logger.Logger._init_logger_format' ) as init_logger_format:
            with patch ( 'googlepostmasterapi.logger.Logger._log_get_logger' ) as log_get_logger:
                with patch ( 'googlepostmasterapi.logger.Logger._init_logger_stdout' ) as init_logger_stdout:
                    with patch ( 'googlepostmasterapi.logger.Logger._init_logger_stderr' ) as init_logger_stderr:
                        with patch ( 'googlepostmasterapi.logger.Logger._log_add_handler' ) as log_add_handler:
                            with patch ( 'googlepostmasterapi.logger.Logger._log_set_level' ) as log_set_level:
                                init_logger_format.return_value = 'random-format';
                                root_logger_mock = Mock (
                                    handlers = 'random-root-logger'
                                );
                                log_get_logger.side_effect = [
                                    root_logger_mock,
                                    'random-logger'
                                ];
                                init_logger_stdout.return_value = 'random-logger-stdout';
                                init_logger_stderr.return_value = 'random-logger-stderr';
                                
                                l = Logger ();

                                ret = l._init_logger ();

                                self.assertEqual ( l._logger, 'random-logger' );

                                init_logger_format.assert_called_once_with ();

                                self.assertEqual ( log_get_logger.call_count, 2 );
                                log_get_logger.assert_any_call ();
                                log_get_logger.assert_any_call (
                                    name = 'Logger'
                                );
                                init_logger_stdout.assert_not_called ();
                                init_logger_stderr.assert_not_called ();
                                log_add_handler.assert_not_called ();
                                log_set_level.assert_called_once_with (
                                    logger = 'random-logger',
                                    level = DEBUG
                                );


if __name__ == '__main__':
    unittest.main ();
