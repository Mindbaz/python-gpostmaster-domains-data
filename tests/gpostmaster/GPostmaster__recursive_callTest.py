#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


class RMock ( GPostmaster ):
    def __init__ ( self, *args, **kargs ):
        print ( 'RMock : __init__' );
        super ().__init__ (
            **kargs
        );
        pass;
        
    def random_method ( self, *args, **kargs ):
        print ( 'RMock : random_method' );
        pass;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__recursive_callTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'tests.gpostmaster.GPostmaster__recursive_callTest.RMock.random_method' ) as random_method:
            random_method.return_value = 'random-returns';
            
            g = RMock (
                token = 'random-token'
            );

            ret = g._recursive_call (
                'random_method',
                'random-arg-1',
                'random-arg-2',
                another_key_1 = 'another-value_1',
                another_key_2 = 'another-value_2'
            );

            self.assertEqual ( ret, 'random-returns' );
            
            random_method.assert_called_once_with (
                'random-arg-1',
                'random-arg-2',
                another_key_1 = 'another-value_1',
                another_key_2 = 'another-value_2'
            );



if __name__ == '__main__':
    unittest.main ();
