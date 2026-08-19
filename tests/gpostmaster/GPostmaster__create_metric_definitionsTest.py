#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__create_metric_definitionsTest ( unittest.TestCase ):
    def test_calls ( self ):
        g = GPostmaster (
            token = 'random-token'
        );

        ret = g._create_metric_definitions ();

        expect = [
            {
                "baseMetric": {
                    "standardMetric": "SPAM_RATE"
                },
                "name": "spam_rate"
            },
            {
                "baseMetric": {
                    "standardMetric": "TLS_ENCRYPTION_RATE"
                },
                "filter": "traffic_direction = \"inbound\"",
                "name": "tls_inbound"
            },
            {
                "baseMetric": {
                    "standardMetric": "FEEDBACK_LOOP_ID"
                },
                "name": "feedback_loop_id"
            },
            {
                "baseMetric": {
                    "standardMetric": "AUTH_SUCCESS_RATE"
                },
                "filter": "auth_type = \"spf\"",
                "name": "auth_spf"
            },
            {
                "baseMetric": {
                    "standardMetric": "AUTH_SUCCESS_RATE"
                },
                "filter": "auth_type = \"dkim\"",
                "name": "auth_dkim"
            },
            {
                "baseMetric": {
                    "standardMetric": "AUTH_SUCCESS_RATE"
                },
                "filter": "auth_type = \"dmarc\"",
                "name": "auth_dmarc"
            },
            {
                "baseMetric": {
                    "standardMetric": "DELIVERY_ERROR_RATE"
                },
                "filter": "error_type = \"reject\" AND error_reason = \"bad_attachment\"",
                "name": "delivery_error__reject__bad_attachment"
            },
            {
                "baseMetric": {
                    "standardMetric": "DELIVERY_ERROR_RATE"
                },
                "filter": "error_type = \"reject\" AND error_reason = \"bad_or_missing_ptr_record\"",
                "name": "delivery_error__reject__bad_or_missing_ptr_record"
            },
            {
                "baseMetric": {
                    "standardMetric": "DELIVERY_ERROR_RATE"
                },
                "filter": "error_type = \"reject\" AND error_reason = \"ip_in_rbls\"",
                "name": "delivery_error__reject__ip_in_rbls"
            },
            {
                "baseMetric": {
                    "standardMetric": "DELIVERY_ERROR_RATE"
                },
                "filter": "error_type = \"reject\" AND error_reason = \"low_domain_reputation\"",
                "name": "delivery_error__reject__low_domain_reputation"
            },
            {
                "baseMetric": {
                    "standardMetric": "DELIVERY_ERROR_RATE"
                },
                "filter": "error_type = \"reject\" AND error_reason = \"low_ip_reputation\"",
                "name": "delivery_error__reject__low_ip_reputation"
            },
            {
                "baseMetric": {
                    "standardMetric": "DELIVERY_ERROR_RATE"
                },
                "filter": "error_type = \"reject\" AND error_reason = \"spammy_content\"",
                "name": "delivery_error__reject__spammy_content"
            },
            {
                "baseMetric": {
                    "standardMetric": "DELIVERY_ERROR_RATE"
                },
                "filter": "error_type = \"reject\" AND error_reason = \"stamp_policy_error\"",
                "name": "delivery_error__reject__stamp_policy_error"
            },
            {
                "baseMetric": {
                    "standardMetric": "DELIVERY_ERROR_RATE"
                },
                "filter": "error_type = \"reject\" AND error_reason = \"other\"",
                "name": "delivery_error__reject__other"
            },
            {
                "baseMetric": {
                    "standardMetric": "DELIVERY_ERROR_RATE"
                },
                "filter": "error_type = \"temp_fail\" AND error_reason = \"anomalous_traffic_pattern\"",
                "name": "delivery_error__temp_fail__anomalous_traffic_pattern"
            },
            {
                "baseMetric": {
                    "standardMetric": "DELIVERY_ERROR_RATE"
                },
                "filter": "error_type = \"temp_fail\" AND error_reason = \"other\"",
                "name": "delivery_error__temp_fail__other"
            }
        ];
        
        self.assertEqual ( ret, expect );


if __name__ == '__main__':
    unittest.main ();
