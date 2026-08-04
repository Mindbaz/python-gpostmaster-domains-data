#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


class FlatData_constructorTest ( unittest.TestCase ):
    def test_constructor ( self ):
        p = FlatData ();

        self.assertEqual ( p.data, {} );
        self.assertEqual ( type ( p._data_tpl ), dict );
        self.assertEqual ( len ( p._data_tpl.keys () ), 9 );
        self.assertEqual ( type ( p.dict_reputation ), dict );
        self.assertEqual ( len ( p.dict_reputation.keys () ), 5 );

        
    def test_data_tpl_values ( self ):
        p = FlatData ();

        ## None
        for k in [ 'user_report_spam_percent', 'domain_reputation', 'auth_use_dkim_percent', 'auth_use_spf_percent', 'auth_use_dmarc_percent', 'tls_inbound_percent' ]:
            self.assertEqual ( p._data_tpl [ k ], None );

        ## FBL
        for k in [ 'feedback_loop' ]:
            self.assertEqual ( p._data_tpl [ k ] [ 'nb_row' ], 0 );
            self.assertEqual ( p._data_tpl [ k ] [ 'percent_per_uid' ], [] );

        ## []
        for k in [ 'delivery_errors', 'ips_reputations' ]:
            self.assertEqual ( p._data_tpl [ k ], [] );

        
    def test_dict_reputation_values ( self ):
        p = FlatData ();

        ## None
        for k in [ 'high', 'medium', 'low', 'bad', 'unknow' ]:
            self.assertEqual ( k in p.dict_reputation, True );
        
        
if __name__ == '__main__':
    unittest.main ();
