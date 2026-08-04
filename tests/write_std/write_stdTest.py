#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.utils import write_std;


class write_stdTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.utils.sys.stdout.write' ) as write:
            write_std ( [
                'random-line-1',
                'random-line-2',
                'random-line-3'
            ] );

            self.assertEqual ( write.call_count, 3 );
            write.assert_any_call ( "random-line-1\n" );
            write.assert_any_call ( "random-line-2\n" );
            write.assert_any_call ( "random-line-3\n" );
