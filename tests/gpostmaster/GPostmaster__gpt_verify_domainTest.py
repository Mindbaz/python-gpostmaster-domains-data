#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googleapiclient.errors import HttpError;
from googlepostmasterapi.gpt import GPostmaster;


class HttpErrorMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'HttpErrorMock : __init__' );
        self.status = 123;
        self.reason = 'random-reason';
        pass;


class RMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'RMock : __init__' );
        pass;

    def domains ( self, *args, **kargs ):
        print ( 'RMock : domains' );
        pass;

    def verify ( self, *args, **kargs ):
        print ( 'RMock : verify' );
        pass;

    def execute ( self, *args, **kargs ):
        print ( 'RMock : execute' );
        pass;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__gpt_verify_domainTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster.write_log' ) as write_log:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster.write_error' ) as write_error:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_verify_domainTest.RMock.domains' ) as domains:
                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_verify_domainTest.RMock.verify' ) as verify:
                        with patch ( 'tests.gpostmaster.GPostmaster__gpt_verify_domainTest.RMock.execute' ) as execute:
                            domains.return_value = RMock ();
                            verify.return_value = RMock ();
                            execute.return_value = 'random-returns';
            
                            g = GPostmaster (
                                token = 'random-token'
                            );
                            g._service = RMock ();
            
                            ret = g._gpt_verify_domain (
                                domain = 'random-domain'
                            );
            
                            self.assertEqual ( ret, True );
                            
                            domains.assert_called_once_with ();
                            verify.assert_called_once_with (
                                name = 'domains/random-domain',
                                body = {
                                    'verificationMethod': 'TXT'
                                }
                            );
                            execute.assert_called_once_with ();
                            write_log.assert_called_with ( [
                                'Verify domain : random-domain'
                            ], force_verbose = True );


    def test_call_raise_exception ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster.write_log' ) as write_log:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster.write_error' ) as write_error:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_verify_domainTest.RMock.domains' ) as domains:
                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_verify_domainTest.RMock.verify' ) as verify:
                        with patch ( 'tests.gpostmaster.GPostmaster__gpt_verify_domainTest.RMock.execute' ) as execute:
                            domains.return_value = RMock ();
                            verify.return_value = RMock ();
                            execute.side_effect = HttpError (
                                HttpErrorMock (),
                                b'random-exception'
                            );
                            
                            g = GPostmaster (
                                token = 'random-token'
                            );
                            g._service = RMock ();
            
                            ret = g._gpt_verify_domain (
                                domain = 'random-domain'
                            );
            
                            self.assertEqual ( ret, False );
                            
                            domains.assert_called_once_with ();
                            verify.assert_called_once_with (
                                name = 'domains/random-domain',
                                body = {
                                    'verificationMethod': 'TXT'
                                }
                            );
                            execute.assert_called_once_with ();
                            write_log.assert_called_once_with ( [
                                'Verify domain : random-domain'
                            ], force_verbose = True );
                            write_error.assert_called_once_with ( [
                                'Unable to verify domain : <HttpError 123 when requesting None returned "random-reason". Details: "random-exception">'
                            ] );


if __name__ == '__main__':
    unittest.main ();
