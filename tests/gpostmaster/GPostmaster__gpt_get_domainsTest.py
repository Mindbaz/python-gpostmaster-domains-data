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
    
    def list ( self, *args, **kargs ):
        print ( 'RMock : list' );
        pass;
    
    def execute ( self, *args, **kargs ):
        print ( 'RMock : execute' );
        pass;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__gpt_get_domainsTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domainsTest.RMock.domains' ) as domains:
            with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domainsTest.RMock.list' ) as list_:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domainsTest.RMock.execute' ) as execute:
                    with patch ( 'googlepostmasterapi.gpt.recursive_call' ) as recursive_call:
                        domains.return_value = RMock ()
                        list_.return_value = RMock ()
                        execute.return_value = 'random-returns';
                        
                        g = GPostmaster (
                            token = 'random-token'
                        );
                        g._service = RMock ();
                        
                        ret = g._gpt_get_domains ();
                        
                        self.assertEqual ( ret, 'random-returns' );
                        domains.assert_called_once_with ();
                        list_.assert_called_once_with (
                            pageToken = None
                        );
                        execute.assert_called_once_with ();
                        recursive_call.assert_not_called ();
                        
                            
    def test_arg_next_page ( self ):
        with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domainsTest.RMock.domains' ) as domains:
            with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domainsTest.RMock.list' ) as list_:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domainsTest.RMock.execute' ) as execute:
                    with patch ( 'googlepostmasterapi.gpt.recursive_call' ) as recursive_call:
                        domains.return_value = RMock ()
                        list_.return_value = RMock ()
                        execute.return_value = 'random-returns'
                        
                        g = GPostmaster (
                            token = 'random-token'
                        );
                        g._service = RMock ();
                        
                        ret = g._gpt_get_domains (
                            next_page = 'random-next-page'
                        );
                        
                        self.assertEqual ( ret, 'random-returns' );
                        domains.assert_called_once_with ();
                        list_.assert_called_once_with (
                            pageToken = 'random-next-page'
                        );
                        execute.assert_called_once_with ();
                        recursive_call.assert_not_called ();
                        
                            
    def test_recursive_on_pagination ( self ):
        with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domainsTest.RMock.domains' ) as domains:
            with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domainsTest.RMock.list' ) as list_:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domainsTest.RMock.execute' ) as execute:
                    with patch ( 'googlepostmasterapi.gpt.recursive_call' ) as recursive_call:
                        domains.return_value = RMock ();
                        list_.return_value = RMock ();
                        execute.return_value = {
                            'nextPageToken': 'random-next-page-token',
                            'domains': [ 'random-domain-1', 'random-domain-2' ]
                        };
                        recursive_call.return_value = {
                            'domains': [ 'random-domain-3' ]
                        };
                        
                        g = GPostmaster (
                            token = 'random-token'
                        );
                        g._service = RMock ();
                        
                        ret = g._gpt_get_domains ();
                        
                        self.assertEqual ( ret, {
                            'nextPageToken': 'random-next-page-token',
                            'domains': [
                                'random-domain-1',
                                'random-domain-2',
                                'random-domain-3'
                            ]
                        } );
                        domains.assert_called_once_with ();
                        list_.assert_called_once_with (
                            pageToken = None
                        );
                        execute.assert_called_once_with ();
                        recursive_call.assert_called_once_with (
                            g._gpt_get_domains,
                            next_page = 'random-next-page-token'
                        );
            
            
if __name__ == '__main__':
    unittest.main ();
