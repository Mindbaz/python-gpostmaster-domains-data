#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import Logger;


class Logger__init_resources_loggerTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.logger.Logger._init_logger' ) as init_logger:
            l = Logger ();
            init_logger.assert_called_once_with ();


if __name__ == '__main__':
    unittest.main ();
