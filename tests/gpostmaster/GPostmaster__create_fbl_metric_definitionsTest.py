#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__create_fbl_metric_definitionsTest ( unittest.TestCase ):
    def test_calls ( self ):
        g = GPostmaster (
            token = 'random-token'
        );

        ret = g._create_fbl_metric_definitions (
            fbl_ids = [
                'random-fbl-id-1',
                'random-fbl-id-2'
            ]
        );

        self.assertEqual ( ret, [
            {
                'name': 'feedback_loop_spam_rate__random-fbl-id-1',
                'baseMetric': {
                    'standardMetric': 'FEEDBACK_LOOP_SPAM_RATE'
                },
                'filter': 'feedback_loop_id = "random-fbl-id-1"'
            },
            {
                'name': 'feedback_loop_spam_rate__random-fbl-id-2',
                'baseMetric': {
                    'standardMetric': 'FEEDBACK_LOOP_SPAM_RATE'
                },
                'filter': 'feedback_loop_id = "random-fbl-id-2"'
            }
        ] );


    def test_no_ids ( self ):
        g = GPostmaster (
            token = 'random-token'
        );

        ret = g._create_fbl_metric_definitions (
            fbl_ids = []
        );

        self.assertEqual ( ret, [] );


if __name__ == '__main__':
    unittest.main ();
