#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;
from googleapiclient.errors import HttpError;


class StatsMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'StatsMock : __init__' );
        pass;
    
    def print_stats ( self, *args, **kargs ):
        print ( 'StatsMock : print_stats' );
        pass;
    

@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__print_statsTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'tests.gpostmaster.GPostmaster__print_statsTest.StatsMock.print_stats' ) as print_stats:
            g = GPostmaster (
                token = 'random-token'
            );
            g._stats = StatsMock ();
            
            g._print_stats ();
            print_stats.assert_called_once_with ();


if __name__ == '__main__':
    unittest.main ();
