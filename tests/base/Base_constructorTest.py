#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.base import Base;


class Base_constructorTest ( unittest.TestCase ):
    def test_constructor ( self ):
        with patch ( 'googlepostmasterapi.logger.Logger.__init__' ) as super_:
            b = Base ();
            
            super_.asser_called_once_with (
                verbose = False
            );

            
    def test_arg_verbose ( self ):
        with patch ( 'googlepostmasterapi.logger.Logger.__init__' ) as super_:
            b = Base (
                verbose = True
            );
            
            super_.asser_called_once_with (
                verbose = True
            );


    def test_inheritance ( self ):
        check = False;
        for inherit in Base.__mro__:
            if ( inherit.__name__ == 'Logger' ):
                check = True;
                break;
        self.assertEqual ( check, True );

                        
            
if __name__ == '__main__':
    unittest.main ();
