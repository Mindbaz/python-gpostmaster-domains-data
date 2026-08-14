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

    def getVerificationToken ( self, *args, **kargs ):
        print ( 'RMock : getVerificationToken' );
        pass;

    def execute ( self, *args, **kargs ):
        print ( 'RMock : execute' );
        pass;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__gpt_get_domain_verify_tokenTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_verify_tokenTest.RMock.domains' ) as domains:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_verify_tokenTest.RMock.getVerificationToken' ) as getVerificationToken:
                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_verify_tokenTest.RMock.execute' ) as execute:
                        domains.return_value = RMock ();
                        getVerificationToken.return_value = RMock ();
                        execute.return_value = {
                            'token': 'random-token-value'
                        };

                        g = GPostmaster (
                            token = 'random-token'
                        );
                        g._service = RMock ();

                        ret = g._gpt_get_domain_verify_token (
                            domain = 'random-domain'
                        );

                        self.assertEqual ( ret, 'random-token-value' );
                        
                        domains.assert_called_once_with ();
                        getVerificationToken.assert_called_once_with (
                            name = 'domains/random-domain/verificationToken',
                            verificationMethod = 'TXT'
                        );
                        execute.assert_called_once_with ();
                        write_std.assert_called_with ( [
                            'Get GPT token for domain : random-domain'
                        ] );


if __name__ == '__main__':
    unittest.main ();
