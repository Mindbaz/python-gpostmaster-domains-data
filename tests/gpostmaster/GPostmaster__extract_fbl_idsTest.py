#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


def r_mock ( value ):
    if ( value == {} ):
        return None;
    if ( value == 'random-value-list-1' ):
        return [
            'random-returns-1', 'random-returns-2'
        ];
    if ( value == 'random-value-list-2' ):
        return [
            'random-returns-1',
            'random-returns-3'
        ];
    return 'Mocked : {}'.format ( value );


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__extract_fbl_idsTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.extract_stat_value' ) as extract_stat_value:
            extract_stat_value.side_effect = r_mock;

            g = GPostmaster (
                token = 'random-token'
            );

            ret = g._extract_fbl_ids (
                domain_stats = [ {
                    'metric': 'feedback_loop_id',
                    'value': 'random-fbl-value-1'
                }, {
                    'metric': 'feedback_loop_id',
                    'value': 999
                }, {
                    'metric': 'feedback_loop_id',
                    'value': 'random-fbl-value-1'
                }, {
                    'metric': 'feedback_loop_id',
                    'value': {}
                } ]
            );

            self.assertEqual ( ret, [
                'Mocked : random-fbl-value-1',
                'Mocked : 999'
            ] );


    def test_calls_with_list ( self ):
        with patch ( 'googlepostmasterapi.gpt.extract_stat_value' ) as extract_stat_value:
            extract_stat_value.side_effect = r_mock;

            g = GPostmaster (
                token = 'random-token'
            );

            ret = g._extract_fbl_ids (
                domain_stats = [ {
                    'metric': 'feedback_loop_id',
                    'value': 'random-value-list-1'
                }, {
                    'metric': 'feedback_loop_id',
                    'value': 'random-value-list-2'
                } ]
            );

            self.assertEqual ( ret, [
                'random-returns-1',
                'random-returns-2',
                'random-returns-3'
            ] );


    def test_no_feedback_loop ( self ):
        g = GPostmaster (
            token = 'random-token'
        );
        
        ret = g._extract_fbl_ids (
            domain_stats = [ {
                'metric': 'another-metric',
                'value':  'another-value'
            } ]
        );

        self.assertEqual ( ret, [] );


if __name__ == '__main__':
    unittest.main ();
