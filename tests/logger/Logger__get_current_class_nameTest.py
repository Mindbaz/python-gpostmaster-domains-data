#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import Logger;


class RMock ( Logger ):
    pass;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger__get_current_class_nameTest ( unittest.TestCase ):
    def test_calls ( self ):
        l = RMock ();

        ret = l._get_current_class_name ();

        self.assertEqual ( ret, 'RMock' );


if __name__ == '__main__':
    unittest.main ();
