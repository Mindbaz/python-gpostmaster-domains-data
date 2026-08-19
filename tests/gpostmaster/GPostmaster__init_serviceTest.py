#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


class RMock ( object ):    
    def __init__ ( self, *args, **kargs ):
        print ( 'RMock : __init__' );
        pass;

    
@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__init_serviceTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._load_token' ) as load_token:
            with patch ( 'googlepostmasterapi.gpt.build' ) as build_:
                load_token.return_value = 'random-data'
                build_.side_effect = RMock;
                
                g = GPostmaster (
                    token = 'random-token'
                );
                
                g._init_service (
                    token = 'another-credentials'
                );
                
                self.assertEqual ( isinstance ( g._service, RMock ), True );
                load_token.assert_called_with (
                    token = 'another-credentials'
                );
                build_.assert_called_with (
                    'gmailpostmastertools',
                    'v2',
                    credentials = 'random-data',
                    static_discovery = False
                );
            
            
if __name__ == '__main__':
    unittest.main ();
