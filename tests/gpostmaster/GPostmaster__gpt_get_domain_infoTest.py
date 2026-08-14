#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock, call;


from googleapiclient.errors import HttpError;
from googlepostmasterapi.gpt import GPostmaster;


class HttpErrorMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'HttpErrorMock : __init__' );
        self.status = 123;
        self.reason = 'random-reason';
        pass;


class StatsMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'StatsMock : __init__' );
        pass;

    def add_ok ( self, *args, **kargs ):
        print ( 'StatsMock : add_ok' );
        pass;

    def add_err_http ( self, *args, **kargs ):
        print ( 'StatsMock : add_err_http' );
        pass;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__gpt_get_domain_infoTest ( unittest.TestCase ):
    def test_calls_without_fbl ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_domain_uri' ) as create_domain_uri:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_metric_definitions' ) as create_metric_definitions:
                    with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_fbl_metric_definitions' ) as create_fbl_metric_definitions:
                        with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_query_request' ) as create_query_request:
                            with patch ( 'googlepostmasterapi.gpt.GPostmaster._query_domain_stats' ) as query_domain_stats:
                                with patch ( 'googlepostmasterapi.gpt.GPostmaster._extract_fbl_ids' ) as extract_fbl_ids:
                                    with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_get_compliance_status' ) as gpt_get_compliance_status:
                                        with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_ok' ) as add_ok:
                                            with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_err_http' ) as add_err_http:
                                                create_domain_uri.return_value = 'random-parent';
                                                create_metric_definitions.return_value = 'random-metric-definitions';
                                                create_query_request.return_value = 'random-body';
                                                query_domain_stats.return_value = [
                                                    'random-domain-stat-1'
                                                ];
                                                extract_fbl_ids.return_value = [];
                                                gpt_get_compliance_status.return_value = 'random-compliance-status';

                                                g = GPostmaster (
                                                    token = 'random-token'
                                                );
                                                g._stats = StatsMock ();

                                                ret = g._gpt_get_domain_info (
                                                    domain = 'random-domain',
                                                    input_date = 'random-input-date'
                                                );

                                                self.assertEqual ( ret [ 'state' ], True );
                                                self.assertEqual ( ret [ 'result' ], {
                                                    'domainStats': [
                                                        'random-domain-stat-1'
                                                    ],
                                                    'complianceStatus': 'random-compliance-status'
                                                } );

                                                create_domain_uri.assert_called_once_with (
                                                    domain = 'random-domain'
                                                );
                                                create_metric_definitions.assert_called_once_with ();
                                                create_query_request.assert_called_once_with (
                                                    input_date = 'random-input-date',
                                                    metric_definitions = 'random-metric-definitions'
                                                );
                                                query_domain_stats.assert_called_once_with (
                                                    parent = 'random-parent',
                                                    body = 'random-body'
                                                );
                                                extract_fbl_ids.assert_called_once_with (
                                                    domain_stats = [
                                                        'random-domain-stat-1'
                                                    ]
                                                );
                                                create_fbl_metric_definitions.assert_not_called ();
                                                gpt_get_compliance_status.assert_called_once_with (
                                                    domain = 'random-domain'
                                                );
                                                write_std.assert_not_called ();
                                                add_ok.assert_called_once_with ();
                                                add_err_http.assert_not_called ();


    def test_calls_with_fbl ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_domain_uri' ) as create_domain_uri:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_metric_definitions' ) as create_metric_definitions:
                    with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_fbl_metric_definitions' ) as create_fbl_metric_definitions:
                        with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_query_request' ) as create_query_request:
                            with patch ( 'googlepostmasterapi.gpt.GPostmaster._query_domain_stats' ) as query_domain_stats:
                                with patch ( 'googlepostmasterapi.gpt.GPostmaster._extract_fbl_ids' ) as extract_fbl_ids:
                                    with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_get_compliance_status' ) as gpt_get_compliance_status:
                                        with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_ok' ) as add_ok:
                                            with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_err_http' ) as add_err_http:
                                                create_domain_uri.return_value = 'random-parent';
                                                create_metric_definitions.return_value = 'random-metric-definitions';
                                                create_fbl_metric_definitions.return_value = 'random-feedback-loop-metric-definitions';
                                                create_query_request.side_effect = [
                                                    'random-body-1',
                                                    'random-body-2'
                                                ];
                                                query_domain_stats.side_effect = [ [
                                                    'random-domain-stat-1'
                                                ], [
                                                    'random-domain-stat-2'
                                                ] ];
                                                extract_fbl_ids.return_value = [
                                                    'random-fbl-1',
                                                    'random-fbl-2'
                                                ];
                                                gpt_get_compliance_status.return_value = 'random-compliance-status';

                                                g = GPostmaster (
                                                    token = 'random-token'
                                                );
                                                g._stats = StatsMock ();

                                                ret = g._gpt_get_domain_info (
                                                    domain = 'random-domain',
                                                    input_date = 'random-input-date'
                                                );

                                                self.assertEqual ( ret [ 'state' ], True );
                                                self.assertEqual ( ret [ 'result' ], {
                                                    'domainStats': [ 'random-domain-stat-1', 'random-domain-stat-2' ],
                                                    'complianceStatus': 'random-compliance-status'
                                                } );

                                                create_fbl_metric_definitions.assert_called_once_with (
                                                    fbl_ids = [
                                                        'random-fbl-1',
                                                        'random-fbl-2'
                                                    ]
                                                );
                                                create_query_request.assert_has_calls ( [
                                                    call ( input_date = 'random-input-date', metric_definitions = 'random-metric-definitions' ),
                                                    call ( input_date = 'random-input-date', metric_definitions = 'random-feedback-loop-metric-definitions' )
                                                ] );
                                                query_domain_stats.assert_has_calls ( [
                                                    call ( parent = 'random-parent', body = 'random-body-1' ),
                                                    call ( parent = 'random-parent', body = 'random-body-2' )
                                                ] );
                                                add_ok.assert_called_once_with ();
                                                add_err_http.assert_not_called ();


    def test_call_raise_exception ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_domain_uri' ) as create_domain_uri:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_metric_definitions' ) as create_metric_definitions:
                    with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_query_request' ) as create_query_request:
                        with patch ( 'googlepostmasterapi.gpt.GPostmaster._query_domain_stats' ) as query_domain_stats:
                            with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_ok' ) as add_ok:
                                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_err_http' ) as add_err_http:
                                    create_domain_uri.return_value = 'random-parent';
                                    query_domain_stats.side_effect = HttpError (
                                        HttpErrorMock (),
                                        b'random-exception'
                                    );

                                    g = GPostmaster (
                                        token = 'random-token'
                                    );
                                    g._stats = StatsMock ();

                                    ret = g._gpt_get_domain_info (
                                        domain = 'random-domain',
                                        input_date = 'random-input-date'
                                    );

                                    self.assertEqual ( ret [ 'state' ], False );
                                    self.assertEqual ( ret [ 'result' ], None );

                                    write_std.assert_not_called ();
                                    add_ok.assert_not_called ();
                                    add_err_http.assert_called_with (
                                        code = 123,
                                        err = 'random-reason',
                                        domain = 'random-domain'
                                    );


    def test_verbose_mode ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_domain_uri' ) as create_domain_uri:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_metric_definitions' ) as create_metric_definitions:
                    with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_query_request' ) as create_query_request:
                        with patch ( 'googlepostmasterapi.gpt.GPostmaster._query_domain_stats' ) as query_domain_stats:
                            with patch ( 'googlepostmasterapi.gpt.GPostmaster._extract_fbl_ids' ) as extract_fbl_ids:
                                with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_get_compliance_status' ) as gpt_get_compliance_status:
                                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_ok' ) as add_ok:
                                        with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_err_http' ) as add_err_http:
                                            create_domain_uri.return_value = 'random-parent';
                                            query_domain_stats.return_value = [
                                                'random-domain-stat-1'
                                            ];
                                            extract_fbl_ids.return_value = [];
                                            gpt_get_compliance_status.return_value = 'random-compliance-status';

                                            g = GPostmaster (
                                                token = 'random-token',
                                                verbose = True
                                            );
                                            g._stats = StatsMock ();

                                            ret = g._gpt_get_domain_info (
                                                domain = 'random-domain',
                                                input_date = 'random-input-date'
                                            );

                                            self.assertEqual ( ret [ 'state' ], True );
                                            write_std.assert_called_with ( [ 'Get domain info : random-domain' ] );
                                            add_ok.assert_called_once_with ();
                                            add_err_http.assert_not_called ();


if __name__ == '__main__':
    unittest.main ();
