#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster_get_domainsTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_get_domains' ) as gpt_get_domains:
                gpt_get_domains.return_value = { 'domains': [
                    { 'name': '/random-domain-1', 'permission': 'random-perm-1' },
                    { 'name': '/random-domain-2', 'permission': 'None' },
                    { 'name': '/random-domain-3', 'permission': 'random-perm-3' }
                ] };
                
                g = GPostmaster (
                    token = 'random-token'
                );
                
                g.get_domains ();
                
                self.assertEqual ( g._domains, [ 'random-domain-1', 'random-domain-3' ] );
                gpt_get_domains.assert_called_once_with ();
                write_std.assert_called_with ( [
                    'Download 2 domain(s) from GPT'
                ] );

                    
    def test_no_domains ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_get_domains' ) as gpt_get_domains:
                gpt_get_domains.return_value = {
                    'domains': []
                };
                
                g = GPostmaster (
                    token = 'random-token'
                );
                
                g.get_domains ();
                
                self.assertEqual ( g._domains, [] );
                gpt_get_domains.assert_called_once_with ();
                write_std.assert_called_with ( [
                    'Download 0 domain(s) from GPT'
                ] );
                
            
if __name__ == '__main__':
    unittest.main ();
