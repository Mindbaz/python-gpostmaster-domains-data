#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;
from googlepostmasterapi.stats import Stats;


class RMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'RMock : __init__' );
        pass;
    
    def register ( self, *args, **kargs ):
        print ( 'RMock : register' );
        pass;
    
    def start ( self, *args, **kargs ):
        print ( 'RMock : start' );
        pass;
    
    def Stats ( self, *args, **kargs ):
        print ( 'RMock : Stats' );
        pass;
    

@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__init_stats_conTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.BaseManager' ) as base_manager:
            with patch ( 'googlepostmasterapi.gpt.BaseManager.register' ) as register:
                with patch ( 'tests.gpostmaster.GPostmaster__init_stats_conTest.RMock.start' ) as start:
                    with patch ( 'tests.gpostmaster.GPostmaster__init_stats_conTest.RMock.Stats' ) as stats:
                        base_manager.side_effect = RMock;
                        stats.return_value = 'random-stats-instance';
                        
                        g = GPostmaster (
                            token = 'random-token'
                        );
                        
                        g._init_stats_con ();
                        
                        self.assertEqual ( g._stats, 'random-stats-instance' );
                        register.assert_called_once_with ( 'Stats', Stats );
                        base_manager.assert_called_once_with ();
                        start.assert_called_once_with ();
                        stats.assert_called_once_with ();
        
            
if __name__ == '__main__':
    unittest.main ();
