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

    def domains ( self, *args, **kargs ):
        print ( 'RMock : domains' );
        pass;

    def getComplianceStatus ( self, *args, **kargs ):
        print ( 'RMock : getComplianceStatus' );
        pass;

    def execute ( self, *args, **kargs ):
        print ( 'RMock : execute' );
        pass;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__gpt_get_compliance_statusTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_compliance_uri' ) as create_compliance_uri:
            with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_compliance_statusTest.RMock.domains' ) as domains:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_compliance_statusTest.RMock.getComplianceStatus' ) as get_compliance_status:
                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_compliance_statusTest.RMock.execute' ) as execute:
                        create_compliance_uri.return_value = 'random-compliance-uri';
                        domains.return_value = RMock ();
                        get_compliance_status.return_value = RMock ();
                        execute.return_value = 'random-returns';

                        g = GPostmaster (
                            token = 'random-token'
                        );
                        g._service = RMock ();

                        ret = g._gpt_get_compliance_status (
                            domain = 'random-domain'
                        );

                        self.assertEqual ( ret, 'random-returns' );
                        create_compliance_uri.assert_called_once_with (
                            domain = 'random-domain'
                        );
                        domains.assert_called_once_with ();
                        get_compliance_status.assert_called_once_with (
                            name = 'random-compliance-uri'
                        );
                        execute.assert_called_once_with ();


if __name__ == '__main__':
    unittest.main ();
