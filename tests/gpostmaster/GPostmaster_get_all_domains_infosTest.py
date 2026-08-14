#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


class PoolMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( '>> PoolMock : __init__' );
        pass;
    
    def __enter__ ( self, *args, **kargs ):
        print ( '>> PoolMock : __enter__' );
        return RMock ();
    
    def __exit__ ( self, *args, **kargs ):
        print ( '>> PoolMock : __exit__' );
        pass;

    
class RMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( '>> RMock : __init__' );
        pass;
    
    def map ( self, *args, **kargs ):
        print ( '>> RMock : map' );
        pass;

        
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster_get_all_domains_infosTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster.get_domains' ) as get_domains:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_pool_data' ) as create_pool_data:
                    with patch ( 'googlepostmasterapi.gpt.Pool' ) as r_init:
                        with patch ( 'tests.gpostmaster.GPostmaster_get_all_domains_infosTest.RMock.map' ) as map_:
                            with patch ( 'googlepostmasterapi.gpt.GPostmaster._clean_pool_returns' ) as clean_pool_returns:
                                with patch ( 'googlepostmasterapi.gpt.GPostmaster._print_stats' ) as print_stats:
                                    create_pool_data.return_value = [
                                        'random-pool-data'
                                    ];
                                    r_init.side_effect = PoolMock;
                                    map_.return_value = 'random-map-returns';
                                    clean_pool_returns.return_value = 'random-cleaned-data';
                                    
                                    g = GPostmaster (
                                        token = 'random-token'
                                    );

                                    ret = g.get_all_domains_infos (
                                        input_date = 'random-input-date'
                                    );

                                    self.assertEqual ( ret, 'random-cleaned-data' );
                                    get_domains.assert_called_once_with ();
                                    create_pool_data.assert_called_with (
                                        input_date = 'random-input-date'
                                    );
                                    r_init.assert_called_with (
                                        processes = 2
                                    );
                                    map_.assert_called_once_with (
                                        g._get_domain_infos_pool,
                                        [ 'random-pool-data' ]
                                    );
                                    clean_pool_returns.assert_called_with (
                                        data = 'random-map-returns'
                                    );
                                    print_stats.assert_called_once_with ();
                                    write_std.assert_not_called ();

                                        
    def test_nothing_to_fecth ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster.get_domains' ) as get_domains:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_pool_data' ) as create_pool_data:
                    with patch ( 'googlepostmasterapi.gpt.Pool' ) as r_init:
                        with patch ( 'tests.gpostmaster.GPostmaster_get_all_domains_infosTest.RMock.map' ) as map_:
                            with patch ( 'googlepostmasterapi.gpt.GPostmaster._clean_pool_returns' ) as clean_pool_returns:
                                with patch ( 'googlepostmasterapi.gpt.GPostmaster._print_stats' ) as print_stats:
                                    create_pool_data.return_value = [];
                                    r_init.side_effect = PoolMock;
                                    map_.return_value = 'random-map-returns';
                                    clean_pool_returns.return_value = 'random-cleaned-data';
                                    
                                    g = GPostmaster (
                                        token = 'random-token'
                                    );

                                    ret = g.get_all_domains_infos (
                                        input_date = 'random-input-date'
                                    );

                                    self.assertEqual ( ret, [] );
                                    get_domains.assert_called_once_with ();
                                    create_pool_data.assert_called_with (
                                        input_date = 'random-input-date'
                                    );
                                    r_init.assert_not_called ();
                                    map_.assert_not_called ();
                                    clean_pool_returns.assert_not_called ();
                                    print_stats.assert_not_called ();
                                    write_std.assert_called_with ( [ 'Nothing to download' ] );

                                    
    def test_arg_pool_size ( self ):
        with patch ( 'googlepostmasterapi.gpt.write_std' ) as write_std:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster.get_domains' ) as get_domains:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._create_pool_data' ) as create_pool_data:
                    with patch ( 'googlepostmasterapi.gpt.Pool' ) as r_init:
                        with patch ( 'tests.gpostmaster.GPostmaster_get_all_domains_infosTest.RMock.map' ) as map_:
                            with patch ( 'googlepostmasterapi.gpt.GPostmaster._clean_pool_returns' ) as clean_pool_returns:
                                with patch ( 'googlepostmasterapi.gpt.GPostmaster._print_stats' ) as print_stats:
                                    create_pool_data.return_value = [
                                        'random-pool-data'
                                    ];
                                    r_init.side_effect = PoolMock;
                                    map_.return_value = 'random-map-returns';
                                    clean_pool_returns.return_value = 'random-cleaned-data';
                                    
                                    g = GPostmaster (
                                        token = 'random-token'
                                    );

                                    ret = g.get_all_domains_infos (
                                        input_date = 'random-input-date',
                                        pool_size = 123
                                    );

                                    self.assertEqual ( ret, 'random-cleaned-data' );
                                    get_domains.assert_called_once_with ();
                                    create_pool_data.assert_called_with (
                                        input_date = 'random-input-date'
                                    );
                                    r_init.assert_called_with (
                                        processes = 123
                                    );
                                    map_.assert_called_once_with (
                                        g._get_domain_infos_pool,
                                        [ 'random-pool-data' ]
                                    );
                                    clean_pool_returns.assert_called_with (
                                        data = 'random-map-returns'
                                    );
                                    print_stats.assert_called_once_with ();
                                    write_std.assert_not_called ();
            
            
if __name__ == '__main__':
    unittest.main ();
