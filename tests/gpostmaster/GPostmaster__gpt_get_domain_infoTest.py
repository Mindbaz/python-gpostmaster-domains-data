#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googleapiclient.errors import HttpError;
from googlepostmasterapi.gpt import GPostmaster;


class RMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'RMock : __init__' );
        pass;
    
    def domains ( self, *args, **kargs ):
        print ( 'RMock : domains' );
        pass;
    
    def trafficStats ( self, *args, **kargs ):
        print ( 'RMock : trafficStats' );
        pass;
    
    def get ( self, *args, **kargs ):
        print ( 'RMock : get' );
        pass;
    
    def execute ( self, *args, **kargs ):
        print ( 'RMock : execute' );
        pass;

    
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
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_domain_uri' ) as create_domain_uri:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.RMock.domains' ) as domains:
                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.RMock.trafficStats' ) as traffic_stats:
                        with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.RMock.get' ) as get:
                            with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.RMock.execute' ) as execute:
                                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_ok' ) as add_ok:            
                                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_err_http' ) as add_err_http:
                                        domains.return_value = RMock ();
                                        traffic_stats.return_value = RMock ();
                                        get.return_value = RMock ();
                                        execute.return_value = 'random-returns';
                                        
                                        g = GPostmaster (
                                            token = 'random-token'
                                        );
                                        g._service = RMock ();
                                        g._stats = StatsMock ();
                                        
                                        ret = g._gpt_get_domain_info (
                                            domain = 'random-domain',
                                            input_date = 'random-input-date'
                                        );
                                        
                                        self.assertEqual ( ret [ 'state' ], True );
                                        self.assertEqual ( ret [ 'result' ], 'random-returns' );
                                        
                                        create_domain_uri.assert_called_with (
                                            domain = 'random-domain',
                                            input_date = 'random-input-date'
                                        );
                                        write_std.assert_not_called ();
                                        add_ok.assert_called_once_with ();
                                        add_err_http.assert_not_called ();

                                    
    def test_call_raise_exception ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_domain_uri' ) as create_domain_uri:
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.RMock.domains' ) as domains:
                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_ok' ) as add_ok:            
                        with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_err_http' ) as add_err_http:
                            domains.side_effect = HttpError ( HttpErrorMock (), b'random-exception' );
                            
                            g = GPostmaster (
                                token = 'random-token'
                            );
                            g._service = RMock ();
                            g._stats = StatsMock ();
                            
                            ret = g._gpt_get_domain_info (
                                domain = 'random-domain',
                                input_date = 'random-input-date'
                            );
                            
                            self.assertEqual ( ret [ 'state' ], False );
                            self.assertEqual ( ret [ 'result' ], None );
                            
                            create_domain_uri.assert_called_with (
                                domain = 'random-domain',
                                input_date = 'random-input-date'
                            );
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
                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.RMock.domains' ) as domains:
                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.RMock.trafficStats' ) as traffic_stats:
                        with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.RMock.get' ) as get:
                            with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.RMock.execute' ) as execute:
                                with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_ok' ) as add_ok:            
                                    with patch ( 'tests.gpostmaster.GPostmaster__gpt_get_domain_infoTest.StatsMock.add_err_http' ) as add_err_http:
                                        domains.return_value = RMock ();
                                        traffic_stats.return_value = RMock ();
                                        get.return_value = RMock ();
                                        execute.return_value = 'random-returns';
                                        
                                        g = GPostmaster (
                                            token = 'random-token',
                                            verbose = True
                                        );
                                        g._service = RMock ();
                                        g._stats = StatsMock ();
                                        
                                        ret = g._gpt_get_domain_info (
                                            domain = 'random-domain',
                                            input_date = 'random-input-date'
                                        );
                                        
                                        self.assertEqual ( ret [ 'state' ], True );
                                        self.assertEqual ( ret [ 'result' ], 'random-returns' );
                                        
                                        create_domain_uri.assert_called_with (
                                            domain = 'random-domain',
                                            input_date = 'random-input-date'
                                        );
                                        write_std.assert_called_with ( [ 'Get domain info : random-domain' ] );
                                        add_ok.assert_called_once_with ();
                                        add_err_http.assert_not_called ();
                                            
            
if __name__ == '__main__':
    unittest.main ();
