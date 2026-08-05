#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


class FlatData_constructorTest ( unittest.TestCase ):
    def test_constructor ( self ):
        f = FlatData ();

        self.assertEqual ( f.data, {} );
        self.assertEqual ( type ( f._data_tpl ), dict );
        self.assertEqual ( len ( f._data_tpl.keys () ), 8 );
        self.assertEqual ( type ( f._compliance_status_tpl ), dict );
        self.assertEqual ( len ( f._compliance_status_tpl.keys () ), 3 );


    def test_data_tpl_values ( self ):
        f = FlatData ();

        ## None
        for k in [ 'user_report_spam_percent', 'domain_compliance', 'auth_use_dkim_percent', 'auth_use_spf_percent', 'auth_use_dmarc_percent', 'tls_inbound_percent' ]:
            self.assertEqual ( f._data_tpl [ k ], None );

        ## FBL
        for k in [ 'feedback_loop' ]:
            self.assertEqual ( f._data_tpl [ k ] [ 'nb_row' ], 0 );
            self.assertEqual ( f._data_tpl [ k ] [ 'percent_per_uid' ], [] );

        ## []
        for k in [ 'delivery_errors' ]:
            self.assertEqual ( f._data_tpl [ k ], [] );


    def test_var_compliance_status_tpl_values ( self ):
        f = FlatData ();

        self.assertEqual ( f._compliance_status_tpl [ 'compliant' ], 'compliant' );
        self.assertEqual ( f._compliance_status_tpl [ 'needs_work' ], 'needs_work' );
        self.assertEqual ( f._compliance_status_tpl [ 'state_unspecified' ], None );


if __name__ == '__main__':
    unittest.main ();
