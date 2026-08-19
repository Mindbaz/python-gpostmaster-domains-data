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

    def addHandler ( self, *args, **kargs ):
        print ( 'RMock : addHandler' );
        pass;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger__log_add_handlerTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'tests.logger.Logger__log_add_handlerTest.RMock.addHandler' ) as addHandler:
            l = Logger ();

            l._log_add_handler (
                logger = RMock (),
                handler = 'random-handler'
            );

            addHandler.assert_called_once_with (
                'random-handler'
            );


if __name__ == '__main__':
    unittest.main ();
