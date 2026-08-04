#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.utils import recursive_call;


def r_mock ( *args, **kargs ):
    pass;


class recursive_callTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'tests.recursive_call.recursive_callTest.r_mock' ) as r_mock:
            r_mock.return_value = 'random-returns';
            
            ret = recursive_call (
                r_mock,
                'random-arg-1',
                'random-arg-2',
                another_key_1 = 'another-value_1',
                another_key_2 = 'another-value_2'
            );
            
            self.assertEqual ( ret, 'random-returns' );
            
            r_mock.assert_called_once_with (
                'random-arg-1',
                'random-arg-2',
                another_key_1 = 'another-value_1',
                another_key_2 = 'another-value_2'
            );
        

if __name__ == '__main__':
    unittest.main ();
