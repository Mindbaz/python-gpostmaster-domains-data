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
    
    def parse ( self, *args, **kargs ):
        print ( 'RMock : parse' );
        pass;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__clean_domain_infosTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'tests.gpostmaster.GPostmaster__clean_domain_infosTest.RMock.parse' ) as parse:
            parse.return_value = 'random-returns';
            
            g = GPostmaster (
                token = 'random-token'
            );
            g._parser = RMock ();
            
            ret = g._clean_domain_infos (
                key = 'random-key',
                data = 'random-data'
            );
            
            self.assertEqual ( ret, 'random-returns' );
            parse.assert_called_with (
                key = 'random-key',
                data = 'random-data'
            );
            
            
if __name__ == '__main__':
    unittest.main ();
