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

    def setFormatter ( self, *args, **kargs ):
        print ( 'RMock : setFormatter' );
        pass;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger__log_set_formatTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'tests.logger.Logger__log_set_formatTest.RMock.setFormatter' ) as setFormatter:
            l = Logger ();

            l._log_set_format (
                logger = RMock (),
                log_format = 'random-log-format'
            );

            setFormatter.assert_called_once_with (
                'random-log-format'
            );


if __name__ == '__main__':
    unittest.main ();
