#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


class GPostmaster__init_resourcesTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_service' ) as init_service:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_parser_con' ) as init_parser_con:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._init_stats_con' ) as init_stats_con:
                    g = GPostmaster (
                        token = 'random-token'
                    );
                    
                    init_service.assert_called_with (
                        token = 'random-token'
                    );
                    init_parser_con.assert_called_once_with ();
                    init_stats_con.assert_called_once_with ();
            
            
if __name__ == '__main__':
    unittest.main ();
