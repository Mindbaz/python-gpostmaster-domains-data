#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.logger import Logger;


class RMock ( object ):
    def __init__ ( self, *args, **kargs ):
        print ( 'RMock : __init__' );
        pass;

    def info ( self, *args, **kargs ):
        print ( 'RMock : info' );
        pass;


@patch ( 'googlepostmasterapi.logger.Logger._init_resources_logger', Mock ( return_value = None ) )
class Logger_write_logTest ( unittest.TestCase ):
    def test_verbose_false_force_false ( self ):
        ## l.verbose = false / force_verbose = false
        with patch ( 'googlepostmasterapi.logger.Logger._get_current_class_name' ) as get_current_class_name:
            with patch ( 'tests.logger.Logger_write_logTest.RMock.info' ) as print_info:
                get_current_class_name.return_value = 'random-class-name';
                
                l = Logger ();
                l.verbose = False;
                l._logger = RMock ();
                
                ret = l.write_log (
                    logs = [
                        'random-log-1',
                        'random-log-2',
                        'random-log-3'
                    ]
                );
                
                self.assertEqual ( ret, False );
                
                print_info.assert_not_called ();


    def test_verbose_true_force_false ( self ):
        ## l.verbose = true / force_verbose = false
        with patch ( 'googlepostmasterapi.logger.Logger._get_current_class_name' ) as get_current_class_name:
             with patch ( 'tests.logger.Logger_write_logTest.RMock.info' ) as print_info:
                 get_current_class_name.return_value = 'random-class-name';
                 
                 l = Logger ();
                 l.verbose = True;
                 l._logger = RMock ();
             
                 ret = l.write_log (
                     logs = [
                         'random-log-1',
                         'random-log-2',
                         'random-log-3'
                     ]
                 );
             
                 self.assertEqual ( ret, True );
             
                 self.assertEqual ( print_info.call_count, 3 );
                 print_info.assert_any_call ( 'random-log-1', extra = { 'class_name': 'random-class-name' } );
                 print_info.assert_any_call ( 'random-log-2', extra = { 'class_name': 'random-class-name' } );
                 print_info.assert_any_call ( 'random-log-3', extra = { 'class_name': 'random-class-name' } );


    def test_verbose_false_force_true ( self ):
        ## l.verbose = false / force_verbose = true
        with patch ( 'googlepostmasterapi.logger.Logger._get_current_class_name' ) as get_current_class_name:
             with patch ( 'tests.logger.Logger_write_logTest.RMock.info' ) as print_info:
                 get_current_class_name.return_value = 'random-class-name';
                 
                 l = Logger ();
                 l.verbose = False;
                 l._logger = RMock ();
             
                 ret = l.write_log (
                     logs = [
                         'random-log-1',
                         'random-log-2',
                         'random-log-3'
                     ],
                     force_verbose = True
                 );
             
                 self.assertEqual ( ret, True );
             
                 self.assertEqual ( print_info.call_count, 3 );
                 print_info.assert_any_call ( 'random-log-1', extra = { 'class_name': 'random-class-name' } );
                 print_info.assert_any_call ( 'random-log-2', extra = { 'class_name': 'random-class-name' } );
                 print_info.assert_any_call ( 'random-log-3', extra = { 'class_name': 'random-class-name' } );


    def test_verbose_true_force_true ( self ):
        ## l.verbose = true / force_verbose = true
        with patch ( 'googlepostmasterapi.logger.Logger._get_current_class_name' ) as get_current_class_name:
             with patch ( 'tests.logger.Logger_write_logTest.RMock.info' ) as print_info:
                 get_current_class_name.return_value = 'random-class-name';
                 
                 l = Logger ();
                 l.verbose = True;
                 l._logger = RMock ();
             
                 ret = l.write_log (
                     logs = [
                         'random-log-1',
                         'random-log-2',
                         'random-log-3'
                     ],
                     force_verbose = True
                 );
             
                 self.assertEqual ( ret, True );
             
                 self.assertEqual ( print_info.call_count, 3 );
                 print_info.assert_any_call ( 'random-log-1', extra = { 'class_name': 'random-class-name' } );
                 print_info.assert_any_call ( 'random-log-2', extra = { 'class_name': 'random-class-name' } );
                 print_info.assert_any_call ( 'random-log-3', extra = { 'class_name': 'random-class-name' } );


if __name__ == '__main__':
    unittest.main ();
