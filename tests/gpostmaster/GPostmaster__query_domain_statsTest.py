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

    def domainStats ( self, *args, **kargs ):
        print ( 'RMock : domainStats' );
        pass;

    def query ( self, *args, **kargs ):
        print ( 'RMock : query' );
        pass;

    def execute ( self, *args, **kargs ):
        print ( 'RMock : execute' );
        pass;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__query_domain_statsTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.domains' ) as domains:
            with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.domainStats' ) as domain_stats:
                with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.query' ) as query:
                    with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.execute' ) as execute:
                        with patch ( 'googlepostmasterapi.gpt.recursive_call' ) as recursive_call:
                            domains.return_value = RMock ();
                            domain_stats.return_value = RMock ();
                            query.return_value = RMock ();
                            execute.return_value = { 'domainStats': [ 'random-domain-stat-1' ] };

                            g = GPostmaster (
                                token = 'random-token'
                            );
                            g._service = RMock ();

                            ret = g._query_domain_stats (
                                parent = 'random-parent',
                                body = { 'random-key': 'random-value' }
                            );

                            self.assertEqual ( ret, [ 'random-domain-stat-1' ] );
                            domains.assert_called_once_with ();
                            domain_stats.assert_called_once_with ();
                            query.assert_called_once_with (
                                parent = 'random-parent',
                                body = { 'random-key': 'random-value' }
                            );
                            execute.assert_called_once_with ();
                            recursive_call.assert_not_called ();


    def test_arg_page_token ( self ):
        with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.domains' ) as domains:
            with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.domainStats' ) as domain_stats:
                with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.query' ) as query:
                    with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.execute' ) as execute:
                        with patch ( 'googlepostmasterapi.gpt.recursive_call' ) as recursive_call:
                            domains.return_value = RMock ();
                            domain_stats.return_value = RMock ();
                            query.return_value = RMock ();
                            execute.return_value = { 'domainStats': [ 'random-domain-stat-1' ] };

                            g = GPostmaster (
                                token = 'random-token'
                            );
                            g._service = RMock ();

                            ret = g._query_domain_stats (
                                parent = 'random-parent',
                                body = { 'random-key': 'random-value' },
                                page_token = 'random-page-token'
                            );

                            self.assertEqual ( ret, [ 'random-domain-stat-1' ] );
                            query.assert_called_once_with (
                                parent = 'random-parent',
                                body = { 'random-key': 'random-value', 'pageToken': 'random-page-token' }
                            );
                            recursive_call.assert_not_called ();


    def test_recursive_on_pagination ( self ):
        with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.domains' ) as domains:
            with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.domainStats' ) as domain_stats:
                with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.query' ) as query:
                    with patch ( 'tests.gpostmaster.GPostmaster__query_domain_statsTest.RMock.execute' ) as execute:
                        with patch ( 'googlepostmasterapi.gpt.recursive_call' ) as recursive_call:
                            domains.return_value = RMock ();
                            domain_stats.return_value = RMock ();
                            query.return_value = RMock ();
                            execute.return_value = {
                                'domainStats': [ 'random-domain-stat-1' ],
                                'nextPageToken': 'random-next-page-token'
                            };
                            recursive_call.return_value = [ 'random-domain-stat-2' ];

                            g = GPostmaster (
                                token = 'random-token'
                            );
                            g._service = RMock ();

                            ret = g._query_domain_stats (
                                parent = 'random-parent',
                                body = { 'random-key': 'random-value' }
                            );

                            self.assertEqual ( ret, [ 'random-domain-stat-1', 'random-domain-stat-2' ] );
                            query.assert_called_once_with (
                                parent = 'random-parent',
                                body = { 'random-key': 'random-value' }
                            );
                            recursive_call.assert_called_once_with (
                                g._query_domain_stats,
                                parent = 'random-parent',
                                body = { 'random-key': 'random-value' },
                                page_token = 'random-next-page-token'
                            );


if __name__ == '__main__':
    unittest.main ();
