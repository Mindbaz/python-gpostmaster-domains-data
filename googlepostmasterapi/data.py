#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Flattens GPT data
# Copyright (C) 2026 Mindbaz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os;
import sys;
import copy;

from pprint import pprint;
from pydantic import validate_call;
from typing import List, Optional;


#: Current module path
MODULE_PATH = os.path.dirname ( os.path.dirname ( os.path.abspath ( __file__ ) ) );
sys.path.insert ( 0, MODULE_PATH );
from googlepostmasterapi.base import Base;


class FlatData ( Base ):
    """Clean data traffic stats from Google Postmaster Tools

    Attributes:
        data (dict): Data cleaned
        _data_tpl (dict): Protected. Template to clean data
        _compliance_status_tpl (dict): Protected. Assoc to translate GPT compliance status to a lowercase string
    """
    @validate_call
    def __init__ ( self ) -> None:
        """Default constructor
        """
        super ().__init__ (
            verbose = True
        );
        
        """Template to clean data"""
        self._data_tpl = {
            'user_report_spam_percent': None,
            'domain_compliance': None,
            'feedback_loop': {
                'nb_row': 0,
                'percent_per_uid': []
            },
            'auth_use_dkim_percent': None,
            'auth_use_spf_percent': None,
            'auth_use_dmarc_percent': None,
            'tls_inbound_percent': None,
            'delivery_errors': []
        };

        """Data cleaned"""
        self.data = {};

        """Assoc to translate GPT compliance status to a lowercase string"""
        self._compliance_status_tpl = {
            'compliant': 'compliant',
            'needs_work': 'needs_work',
            'state_unspecified': None
        };


    def _index_domain_stats ( self, domain_stats: List [ dict ] ) -> dict:
        """Index a list of DomainStat objects by their metric name

        Arguments:
            domain_stats (dict[]): List of DomainStat objects

        Returns:
            dict: Assoc metric name => extracted value
        """
        return {
            domain_stat [ 'metric' ]: self.extract_stat_value ( value = domain_stat.get ( 'value', {} ) )
            for domain_stat in domain_stats
            if ( 'metric' in domain_stat )
        };


    def _parse_user_report_spam ( self, key: str, value: Optional [ float ] = None ) -> bool:
        """Clean part of metric : spam_rate

        Arguments:
            key (str): Key to identify data
            value (float): Optional. Spam rate to convert to percent. Default : None

        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( value == None ):
            return False;
        self.data [ key ] [ 'user_report_spam_percent' ] = round (
            float ( value ) * 100.0,
            2
        );
        return True;


    def _parse_status ( self, status: Optional [ dict ] = None ) -> Optional [ str ]:
        """Clean a ComplianceStatus object to a lowercase string

        Arguments:
            status (dict): Optional. ComplianceStatus object. Default : None

        Returns:
            str: Cleaned status. None if no status set
        """
        if ( status == None ):
            return None;

        if ( ( 'status' in status ) == False ):
            return None;
        
        return self._compliance_status_tpl.get (
            status [ 'status' ].lower (),
            None
        );


    def _parse_domain_compliance ( self, key: str, value: Optional [ dict ] = None ) -> bool:
        """Clean part of key : complianceStatus.complianceData

        Arguments:
            key (str): Key to identify data
            value (dict): Optional. DomainComplianceData object. Default : None

        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( value == None ):
            return False;

        """Deliverability status"""
        deliverability = value.get ( 'deliverabilityStatusVerdict', {} );
        """One-click unsubscribe"""
        one_click_unsubscribe = value.get ( 'oneClickUnsubscribeVerdict', {} );
        """Honor unsubscribe"""
        honor_unsubscribe = value.get ( 'honorUnsubscribeVerdict', {} );

        self.data [ key ] [ 'domain_compliance' ] = {
            'deliverability': {
                'status': self._parse_status (
                    status = deliverability.get ( 'state' )
                ),
                'reason': deliverability.get ( 'reason' )
            },
            'one_click_unsubscribe': {
                'status': self._parse_status (
                    status = one_click_unsubscribe.get ( 'status' )
                ),
                'reason': one_click_unsubscribe.get ( 'reason' )
            },
            'honor_unsubscribe': {
                'status': self._parse_status (
                    status = honor_unsubscribe.get ( 'status' )
                ),
                'reason': honor_unsubscribe.get ( 'reason' )
            },
            'checks': [ {
                'check': row.get ( 'requirement' ),
                'status': self._parse_status (
                    status = row.get ( 'status' )
                ) }
                for row in value.get ( 'rowData', [] )
            ]
        };
        
        return True;


    def _parse_fbl ( self, key: str, value: dict ) -> bool:
        """Clean part of metric : feedback_loop_spam_rate__{id}

        Arguments:
            key (str): Key to identify data
            value (dict): Assoc feedback loop id => spam rate

        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( len ( value ) == 0 ):
            return False;

        for feedback_loop_id in value:
            if ( value [ feedback_loop_id ] == None ):
                ## Missing data from gpostmasters
                continue;

            self.data [ key ] [ 'feedback_loop' ] [ 'nb_row' ] += 1;
            self.data [ key ] [ 'feedback_loop' ] [ 'percent_per_uid' ].append ( {
                'uid': int ( feedback_loop_id ) if feedback_loop_id.isdigit () else feedback_loop_id,
                'spam_percent': round (
                    float ( value [ feedback_loop_id ] ) * 100.0,
                    2
                )
            } );

        return True;


    def _parse_use_auth ( self, key: str, **kargs: dict ) -> bool:
        """Clean part of metrics : auth_dkim / auth_spf / auth_dmarc

        Arguments:
            key (str): Key to identify data
            dkim (float): Optional. DKIM success rate to convert to percent
            spf (float): Optional. SPF success rate to convert to percent
            dmarc (float): Optional. DMARC success rate to convert to percent

        Returns:
            bool: True if at leat one the three key exists. False otherwise
        """
        """Flag to valid at least one value"""
        ret = False;

        for karg in [ 'dkim', 'spf', 'dmarc' ]:
            if ( karg not in kargs ):
                ## Karg not exists
                continue;
            if ( kargs [ karg ] == None ):
                ## Value None
                continue;
            ret = True;
            
            self.data [ key ] [
                'auth_use_{}_percent'.format ( karg )
            ] = round (
                float ( kargs [ karg ] ) * 100.0,
                2
            );

        return ret;


    def _parse_crypted_inbound ( self, key: str, value: Optional [ float ] = None ) -> bool:
        """Clean part of metric : tls_inbound

        Arguments:
            key (str): Key to identify data
            value (float): Optional. Inbound TLS encryption rate to convert to percent. Default : None

        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( value == None ):
            return False;
        self.data [ key ] [ 'tls_inbound_percent' ] = round (
            float ( value ) * 100.0,
            2
        );
        return True;


    def _parse_delivery_err ( self, key: str, value: dict ) -> bool:
        """Clean part of metrics : delivery_error__{class}__{type}

        Arguments:
            key (str): Key to identify data
            value (dict): Assoc '{class}__{type}' => error rate

        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( len ( value ) == 0 ):
            return False;
        
        for error_key in value:
            if ( value [ error_key ] == None ):
                ## No data for this class/type on this domain/date
                continue;
            
            if ( value [ error_key ] == 0 ):
                ## Empty data for this class/type on this domain/date
                continue;

            """Error class & type"""
            error_class, error_type = error_key.split ( '__', 1 );
            
            self.data [ key ] [ 'delivery_errors' ].append ( {
                'class': error_class,
                'type': error_type,
                'percent': round (
                    float ( value [ error_key ] ) * 100.0,
                    2
                )
            } );

        return True;


    @validate_call
    def parse ( self, key: str, data: dict ) -> dict:
        """Parse data from GPT to a flatern version with all values

        Arguments:
            key (str): Key to identify data
            data (dict): Data from GPT to clean, format : { 'domainStats': [ ... ], 'complianceStatus': { ... } }

        Returns:
            dict: Cleaned data from GPT
        """

        """Current key data"""
        self.data [ key ] = copy.deepcopy (
            self._data_tpl
        );

        """Domain stats indexed by metric name"""
        stats = self._index_domain_stats (
            domain_stats = data.get ( 'domainStats', [] )
        );

        ## Clean : spam_rate
        self._parse_user_report_spam (
            key = key,
            value = stats.get ( 'spam_rate' )
        );
        
        """Compliance status, root object"""
        compliance_status = data.get ( 'complianceStatus', {} );

        ## Clean : complianceStatus.subdomainComplianceData if the queried name is a subdomain, else complianceStatus.complianceData
        self._parse_domain_compliance (
            key = key,
            value = compliance_status.get ( 'subdomainComplianceData' ) or compliance_status.get ( 'complianceData' )
        );
        
        ## Clean : feedback_loop_spam_rate__{id}
        self._parse_fbl (
            key = key,
            value = {
                metric_name [ len ( 'feedback_loop_spam_rate__' ) : ]: value
                for metric_name, value in stats.items ()
                if metric_name.startswith ( 'feedback_loop_spam_rate__' )
            }
        );
        
        ## Clean : auth_dkim / auth_spf / auth_dmarc
        self._parse_use_auth (
            key = key,
            dkim = stats.get ( 'auth_dkim' ),
            spf = stats.get ( 'auth_spf' ),
            dmarc = stats.get ( 'auth_dmarc' )
        );
        
        ## Clean : tls_inbound
        self._parse_crypted_inbound (
            key = key,
            value = stats.get ( 'tls_inbound' )
        );
        
        ## Clean : delivery_error__{class}__{type}
        self._parse_delivery_err (
            key = key,
            value = {
                metric_name [ len ( 'delivery_error__' ) : ]: value
                for metric_name, value in stats.items ()
                if metric_name.startswith ( 'delivery_error__' )
            }
        );

        """Cleaned data from GPT"""
        ret = copy.deepcopy (
            self.data [ key ]
        );

        ## Clean data
        del ( self.data [ key ] );

        return ret;
