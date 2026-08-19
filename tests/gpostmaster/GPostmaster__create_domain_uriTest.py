#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__create_domain_uriTest ( unittest.TestCase ):
    def test_calls ( self ):
        g = GPostmaster (
            token = 'random-token'
        );
        g._uri_tpl = 'random uri with : {domain}';

        ret = g._create_domain_uri (
            domain = 'random-domain'
        );

        self.assertEqual ( ret, 'random uri with : random-domain' );
            
            
if __name__ == '__main__':
    unittest.main ();
