#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import Logger;


class Logger_constructorTest ( unittest.TestCase ):
    def test_constructor ( self ):
        with patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger' ) as init_resources_logger:
            l = Logger ();
            
            self.assertEqual ( l.verbose, False );
            self.assertTrue ( type ( l._log_tpl ) is dict );
            
            init_resources_logger.assert_called_once_with ();

            
    def test_verbose ( self ):
        with patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger' ) as init_resources_logger:
            l = Logger (
                verbose = True
            );
            
            self.assertEqual ( l.verbose, True );
            
            init_resources_logger.assert_called_once_with ();


    def test_log_tpl ( self ):
        with patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger' ) as init_resources_logger:
            l = Logger ();

            for k in [ 'base', 'ts' ]:
                self.assertTrue ( type ( l._log_tpl [ k ] ) is str, k );
                self.assertTrue ( len ( l._log_tpl [ k ] ) > 0, k );
            
            init_resources_logger.assert_called_once_with ();

        
if __name__ == '__main__':
    unittest.main ();
