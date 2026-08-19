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

    def setLevel ( self, *args, **kargs ):
        print ( 'RMock : setLevel' );
        pass;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger__log_set_levelTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'tests.logger.Logger__log_set_levelTest.RMock.setLevel' ) as setLevel:
            l = Logger ();

            l._log_set_level (
                logger = RMock (),
                level = 123
            );

            setLevel.assert_called_once_with (
                123
            );


if __name__ == '__main__':
    unittest.main ();
