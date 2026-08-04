#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__init_parser_conTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.FlatData' ) as r_init:
            g = GPostmaster (
                token = 'random-token'
            );
            
            g._init_parser_con ();
            self.assertEqual ( isinstance ( g._parser, Mock ), True );
            r_init.assert_called_once_with ();


if __name__ == '__main__':
    unittest.main ();
