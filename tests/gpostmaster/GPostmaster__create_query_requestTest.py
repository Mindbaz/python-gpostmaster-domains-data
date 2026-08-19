#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__create_query_requestTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._parse_input_date' ) as parse_input_date:
            parse_input_date.return_value = { 'year': 2026, 'month': 8, 'day': 4 };

            g = GPostmaster (
                token = 'random-token'
            );

            ret = g._create_query_request (
                input_date = 'random-input-date',
                metric_definitions = [ 'random-metric-definition-1', 'random-metric-definition-2' ]
            );

            self.assertEqual ( ret, {
                'timeQuery': { 'dateList': { 'dates': [ { 'year': 2026, 'month': 8, 'day': 4 } ] } },
                'aggregationGranularity': 'DAILY',
                'metricDefinitions': [ 'random-metric-definition-1', 'random-metric-definition-2' ],
                'pageSize': 200
            } );
            parse_input_date.assert_called_once_with (
                input_date = 'random-input-date'
            );


if __name__ == '__main__':
    unittest.main ();
