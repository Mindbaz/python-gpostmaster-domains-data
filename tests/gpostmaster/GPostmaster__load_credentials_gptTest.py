#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;

from googlepostmasterapi.gpt import GPostmaster;


class HandleMock ( object ):    
    def read ( self, *args, **kargs ):
        print ( 'HandleMock : read' );
        pass;


class OpenMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'OpenMock : __init__' );
        pass;
    
    def __open__ ( self, *args, **kargs ):
        print ( 'OpenMock : __open__' );
        pass;
    
    def __enter__ ( self, *args, **kargs ):
        print ( 'OpenMock : __enter__' );
        return HandleMock;
    
    def __exit__ ( self, *args, **kargs ):
        print ( 'OpenMock : __exit__' );
        pass;

    
class PickleMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'OpenMock : __init__' );
        pass;
    
    def load ( self, *args, **kargs ):
        print ( 'OpenMock : load' );
        pass;


@patch ( 'googlepostmasterapi.gpt.pickle', PickleMock )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__load_tokenTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.open' ) as open_:
            with patch ( 'googlepostmasterapi.gpt.pickle.load' ) as load_:
                open_.side_effect = OpenMock;
                load_.return_value = 'random-returns';
                
                g = GPostmaster (
                    token = 'random-token'
                );
                
                ret = g._load_token (
                    token = 'another-credentials'
                );
                
                self.assertEqual ( ret, 'random-returns' );
                open_.asser_called_with (
                    'another-credentials',
                    'rb'
                );
                load_.assert_called_once_with ( HandleMock );

            
if __name__ == '__main__':
    unittest.main ();
