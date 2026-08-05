#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;
import random;


def get_status ( i ):
    return random.choice (
        list (
            i._compliance_status_tpl.keys ()
        )
    );
    

class FlatData__parse_statusTest ( unittest.TestCase ):
    def test_compliant ( self ):
        f = FlatData ();

        in_s = get_status ( f );
        
        ret = f._parse_status (
            status = { 'status': in_s.upper () }
        );
        
        self.assertEqual ( ret, f._compliance_status_tpl [ in_s ] );


    def test_no_status_key ( self ):
        f = FlatData ();

        ret = f._parse_status (
            status = {}
        );

        self.assertEqual ( ret, None );


    def test_no_value ( self ):
        f = FlatData ();

        ret = f._parse_status (
            status = None
        );

        self.assertEqual ( ret, None );


if __name__ == '__main__':
    unittest.main ();
