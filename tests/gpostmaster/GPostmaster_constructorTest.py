#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


class GPostmaster_constructorTest ( unittest.TestCase ):
    def test_constructor ( self ):
        with patch ( 'googlepostmasterapi.base.Base.__init__' ) as super_:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources' ) as init_ressources:
                g = GPostmaster (
                    token = 'random-token'
                );
                
                self.assertEqual ( type ( g._uri_tpl ), str );
                self.assertEqual ( type ( g._compliance_uri_tpl ), str );
                self.assertEqual ( type ( g._delivery_error_reasons ), dict );
                self.assertEqual ( g._domains, [] );
                self.assertEqual ( type ( g.scopes ), list );

                super_.assert_called_with (
                    verbose = False
                );
                init_ressources.assert_called_with (
                    token = 'random-token'
                );


    def test_arg_verbose ( self ):
        with patch ( 'googlepostmasterapi.base.Base.__init__' ) as super_:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources' ) as init_ressources:
                g = GPostmaster (
                    token = 'random-token',
                    verbose = True
                );
                
                super_.assert_called_with (
                    verbose = True
                );
              
                
    def test_var__uri_tpl ( self ):
        with patch ( 'googlepostmasterapi.base.Base.__init__' ) as super_:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources' ) as init_ressources:
                g = GPostmaster (
                    token = 'random-token',
                    verbose = True
                );
                
                self.assertTrue ( len ( g._uri_tpl ) > 0 );
                self.assertTrue ( '{domain}' in g._uri_tpl );
              
                
    def test_var__compliance_uri_tpl ( self ):
        with patch ( 'googlepostmasterapi.base.Base.__init__' ) as super_:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources' ) as init_ressources:
                g = GPostmaster (
                    token = 'random-token',
                    verbose = True
                );
                
                self.assertTrue ( len ( g._compliance_uri_tpl ) > 0 );
                self.assertTrue ( '{domain}' in g._compliance_uri_tpl );
              
                
    def test_var__delivery_error_reasons ( self ):
        with patch ( 'googlepostmasterapi.base.Base.__init__' ) as super_:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources' ) as init_ressources:
                g = GPostmaster (
                    token = 'random-token',
                    verbose = True
                );
            
                for k in [ 'reject', 'temp_fail' ]:
                    self.assertTrue ( k in g._delivery_error_reasons, k );
                    self.assertEqual ( type ( g._delivery_error_reasons [ k ] ), list, k );
                    self.assertTrue ( len ( g._delivery_error_reasons [ k ] ) > 0, k );
                    
                    for v in g._delivery_error_reasons [ k ]:
                        self.assertEqual ( type ( v ), str, v );
              
                
    def test_var_scopes ( self ):
        with patch ( 'googlepostmasterapi.base.Base.__init__' ) as super_:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources' ) as init_ressources:
                g = GPostmaster (
                    token = 'random-token',
                    verbose = True
                );
            
                self.assertTrue ( len ( g.scopes ) > 0 );
                
                for k in g.scopes:
                    self.assertEqual ( type ( k ), str, k );


    def test_inheritance ( self ):
        check = False;
        for inherit in GPostmaster.__mro__:
            if ( inherit.__name__ == 'Base' ):
                check = True;
                break;
        self.assertEqual ( check, True );
        
        
if __name__ == '__main__':
    unittest.main ();
