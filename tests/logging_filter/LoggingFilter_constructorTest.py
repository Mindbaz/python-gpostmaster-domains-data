#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import LoggingFilter;


class LoggingFilter_constructorTest ( unittest.TestCase ):
    def test_constructor ( self ):
        l = LoggingFilter (
            level = 123
        );
        
        self.assertEqual ( l.max_level, 123 );

        
if __name__ == '__main__':
    unittest.main ();
