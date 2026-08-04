#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


class GPostmaster_constructorTest ( unittest.TestCase ):
    def test_constructor ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources' ) as init_ressources:
            g = GPostmaster (
                token = 'random-token'
            );
            
            init_ressources.assert_called_with (
                token = 'random-token'
            );
            
            self.assertEqual ( g.verbose, False );
            self.assertEqual ( type ( g._uri_tpl ), str );
            self.assertEqual ( len ( g._uri_tpl ) > 0, True );
            self.assertEqual ( g._domains, [] );
            self.assertEqual ( g._pool_size, 2 );

                
    def test_pool_size ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources' ) as init_ressources:
            g = GPostmaster (
                token = 'random-token',
                pool_size = '951'
            );
            self.assertEqual ( g._pool_size, 951 );
              
                
    def test_verbose ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources' ) as init_ressources:
            g = GPostmaster (
                token = 'random-token',
                verbose = True
            );
            self.assertEqual ( g.verbose, True );
        
        
if __name__ == '__main__':
    unittest.main ();
