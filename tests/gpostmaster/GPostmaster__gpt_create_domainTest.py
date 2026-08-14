#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;
from googleapiclient.errors import HttpError;


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

    def create ( self, *args, **kargs ):
        print ( 'RMock : create' );
        pass;

    def execute ( self, *args, **kargs ):
        print ( 'RMock : execute' );
        pass;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__gpt_create_domainTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'tests.gpostmaster.GPostmaster__gpt_create_domainTest.RMock.domains' ) as domains:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_create_domainTest.RMock.create' ) as create:
                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_create_domainTest.RMock.execute' ) as execute:
                        domains.return_value = RMock ();
                        create.return_value = RMock ();
                        execute.return_value = 'random-returns';

                        g = GPostmaster (
                            token = 'random-token'
                        );
                        g._service = RMock ();

                        ret = g._gpt_create_domain (
                            domain = 'random-domain'
                        );

                        self.assertEqual ( ret, True );
                        
                        domains.assert_called_once_with ();
                        create.assert_called_once_with (
                            body = {
                                'domainId': 'random-domain'
                            }
                        );
                        execute.assert_called_once_with ();
                        write_std.assert_called_with ( [
                            'Add domain to GPT : random-domain'
                        ] );


    def test_call_raise_exception ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'tests.gpostmaster.GPostmaster__gpt_create_domainTest.RMock.domains' ) as domains:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_create_domainTest.RMock.create' ) as create:
                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_create_domainTest.RMock.execute' ) as execute:
                        domains.return_value = RMock ();
                        create.return_value = RMock ();
                        execute.side_effect = HttpError (
                            HttpErrorMock (), b'random-exception'
                        );

                        g = GPostmaster (
                            token = 'random-token'
                        );
                        g._service = RMock ();

                        ret = g._gpt_create_domain (
                            domain = 'random-domain'
                        );

                        self.assertEqual ( ret, False );
                        
                        domains.assert_called_once_with ();
                        create.assert_called_once_with (
                            body = {
                                'domainId': 'random-domain'
                            }
                        );
                        execute.assert_called_once_with ();
                        self.assertEqual ( write_std.call_count, 2 );
                        write_std.assert_any_call ( [
                            'Add domain to GPT : random-domain'
                        ] );
                        write_std.assert_any_call ( [
                            'Error while adding domain to GPT : <HttpError 123 when requesting None returned "random-reason". Details: "random-exception">'
                        ] );


if __name__ == '__main__':
    unittest.main ();
