#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Downloads and flattens data from GPT
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
import json;

from google.oauth2.credentials import Credentials;
from googleapiclient.discovery import build;
from googleapiclient.errors import HttpError;
from multiprocessing import Pool;
from multiprocessing.managers import BaseManager;
from pprint import pprint;
from pydantic import validate_call;
from typing import Any, List, Optional;


#: Current module path
MODULE_PATH = os.path.dirname ( os.path.dirname ( os.path.abspath ( __file__ ) ) );
sys.path.insert ( 0, MODULE_PATH );
from googlepostmasterapi.data import FlatData;
from googlepostmasterapi.stats import Stats;
from googlepostmasterapi.utils import extract_stat_value, recursive_call, write_std;


class GPostmaster ( object ):
    """Download data from Google postmaster tools

    Attributes:
        _uri_tpl (str): Protected. Template to create a domain parent uri
        _compliance_uri_tpl (str): Protected. Template to create a domain compliance status uri
        _delivery_error_reasons (dict): Protected. Assoc of error_type to the list of error_reason supported by GPT v2
        _domains (str[]): Protected. All domains download from server
        _service (googleapiclient.discovery.build): Protected. Connector to GPT
        _parser (FlatData): Protected. Connector to data cleaner
        _stats (Stats): Protected. Connector to statistiques data
        _pool_size (int): Protected. Number of threads
        scopes (str[]): GPT scopes to read data
    """
    @validate_call
    def __init__ ( self, token: str, pool_size: Optional [ int ] = 2, verbose: Optional [ bool ] = False ) -> None:
        """Default constructor

        Arguments:
            token (str): Local file path to GPT json token
            pool_size (int): Optional. Number of threads. Default : 2
            verbose (bool): Optional. Verbose mode. Default : False
        """
        """Verbose mode"""
        self.verbose = verbose;

        """Template to create a domain parent uri"""
        self._uri_tpl = 'domains/{domain}';

        """Template to create a domain compliance status uri"""
        self._compliance_uri_tpl = 'domains/{domain}/complianceStatus';

        """Assoc of error_type to the list of error_reason supported by GPT v2 : DELIVERY_ERROR_RATE"""
        self._delivery_error_reasons = {
            'reject': [
                'bad_attachment',
                'bad_or_missing_ptr_record',
                'ip_in_rbls',
                'low_domain_reputation',
                'low_ip_reputation',
                'spammy_content',
                'stamp_policy_error',
                'other'
            ],
            'temp_fail': [
                'anomalous_traffic_pattern',
                'other'
            ]
        };

        """All domains download from server"""
        self._domains = [];

        """Number of threads"""
        self._pool_size = pool_size;
        
        """GPT scopes to read data"""
        self.scopes = [
            'https://www.googleapis.com/auth/postmaster.domain',
            'https://www.googleapis.com/auth/postmaster.traffic.readonly'
        ];

        self._init_resources (
            token = token
        );


    def _init_resources ( self, token: str ) -> None:
        """Init resources used by system : init service / parser / stats

        Arguments:
            token (str): Local file path to GPT json token
        """
        ## Init service
        self._init_service (
            token = token
        );

        ## Init parser
        self._init_parser_con ();

        ## Init stats
        self._init_stats_con ();


    def _init_stats_con ( self ) -> None:
        """Init stats con. Should be manager by multiprocessing to work with pool
        """
        BaseManager.register ( 'Stats', Stats );
        """Multiprocessing manager to share Stats between all threads"""
        manager = BaseManager ();
        manager.start ();
        """Connector to statistiques data"""
        self._stats = manager.Stats ();


    def _load_token ( self, token: str ) -> Credentials:
        """Load GPT token

        Arguments:
            token (str): Local file path to GPT json token

        Returns:
            Credentials: GPT creds
        """
        return Credentials.from_authorized_user_file (
            token,
            self.scopes
        );


    def _init_service ( self, token: str ) -> None:
        """Init service connector

        Arguments:
            token (str): Local file path to GPT json token
        """
        """Connector to Google Postmaster Tools"""
        self._service = build (
            'gmailpostmastertools',
            'v2',
            credentials = self._load_token (
                token = token
            )
        );


    def _gpt_get_domains ( self, next_page: Optional [ str ] = None ) -> List [ dict ]:
        """Call GPT to get all domains. Recursive call on pagination

        Arguments:
            next_page (str): Optional. Token to get next page of domains. Default : None

        Returns:
            list: List of dict with all domains, format : [ { 'name': ..., 'createTime': ..., 'permission': ... } ]
        """
        """All domains"""
        ret = self._service.domains ().list (
            pageToken = next_page
        ).execute ();

        if ( 'nextPageToken' in ret ):
            """Domains from next page. Recursive call"""
            tmp = recursive_call (
                self._gpt_get_domains,
                next_page = ret [ 'nextPageToken' ]
            );
            ret [ 'domains' ] += tmp [ 'domains' ];

        return ret;


    @validate_call
    def get_domains ( self ) -> None:
        """Get all domains with permissions : owner/reader
        """
        """All domains infos from GPT"""
        domains = self._gpt_get_domains ();

        for domain_data in domains [ 'domains' ]:
            if ( domain_data [ 'permission' ].lower () == 'none' ):
                continue;
            self._domains.append ( domain_data [ 'name' ].split ( '/' ).pop () );

        write_std ( [
            'Downloaded {} domain(s) from GPT'.format ( len ( self._domains ) )
        ] );


    def _create_domain_uri ( self, domain: str ) -> str:
        """Create parent uri to a domain to query

        Arguments:
            domain (str): Domain to query

        Returns:
            str: Parent uri, format : domains/{domain}
        """
        return self._uri_tpl.format (
            domain = domain
        );


    def _create_compliance_uri ( self, domain: str ) -> str:
        """Create uri to a domain compliance status to query

        Arguments:
            domain (str): Domain to query

        Returns:
            str: Compliance status uri, format : domains/{domain}/complianceStatus
        """
        return self._compliance_uri_tpl.format (
            domain = domain
        );


    def _parse_input_date ( self, input_date: str ) -> dict:
        """Parse an input date to a GPT Date object

        Arguments:
            input_date (str): Date to query, format : YYYYMMDD

        Returns:
            dict: GPT Date object, format : { 'year': int, 'month': int, 'day': int }
        """
        return {
            'year': int ( input_date [ 0 : 4 ] ),
            'month': int ( input_date [ 4 : 6 ] ),
            'day': int ( input_date [ 6 : 8 ] )
        };


    def _create_metric_definitions ( self ) -> List [ dict ]:
        """Create the list of metric definitions to query on domainStats : spam rate / auth / tls inbound / delivery errors / feedback loop id

        Returns:
            dict[]: List of MetricDefinition objects
        """
        """Metric definitions to query"""
        metrics = [
            {
                'name': 'spam_rate',
                'baseMetric': {
                    'standardMetric': 'SPAM_RATE'
                }
            },
            {
                'name': 'tls_inbound',
                'baseMetric': {
                    'standardMetric': 'TLS_ENCRYPTION_RATE'
                },
                'filter': 'traffic_direction = "inbound"'
            },
            {
                'name': 'feedback_loop_id',
                'baseMetric': {
                    'standardMetric': 'FEEDBACK_LOOP_ID'
                }
            }
        ];

        for auth_type in [ 'spf', 'dkim', 'dmarc' ]:
            metrics.append ( {
                'name': 'auth_{type_}'.format (
                    type_ = auth_type
                ),
                'baseMetric': {
                    'standardMetric': 'AUTH_SUCCESS_RATE'
                },
                'filter': 'auth_type = "{}"'.format ( auth_type )
            } );

        for error_type in self._delivery_error_reasons:
            for error_reason in self._delivery_error_reasons [ error_type ]:
                metrics.append ( {
                    'name': 'delivery_error__{type_}__{reason}'.format (
                        type_ = error_type,
                        reason = error_reason
                    ),
                    'baseMetric': {
                        'standardMetric': 'DELIVERY_ERROR_RATE'
                    },
                    'filter': 'error_type = "{type_}" AND error_reason = "{reason}"'.format (
                        type_ = error_type,
                        reason = error_reason
                    )
                } );

        return metrics;


    def _create_fbl_metric_definitions ( self, fbl_ids: List [ str ] ) -> List [ dict ]:
        """Create the list of metric definitions to query the spam rate of each feedback loop id

        Arguments:
            fbl_ids (str[]): Feedback loop ids to query

        Returns:
            dict[]: List of MetricDefinition objects
        """
        return [
            {
                'name': 'feedback_loop_spam_rate__{}'.format ( fbl_id ),
                'baseMetric': { 'standardMetric': 'FEEDBACK_LOOP_SPAM_RATE' },
                'filter': 'feedback_loop_id = "{}"'.format ( fbl_id )
            }
            for fbl_id in fbl_ids
        ];


    def _create_query_request ( self, input_date: str, metric_definitions: List [ dict ] ) -> dict:
        """Create a QueryDomainStatsRequest body

        Arguments:
            input_date (str): Date to query, format : YYYYMMDD
            metric_definitions (dict[]): List of MetricDefinition objects to query

        Returns:
            dict: QueryDomainStatsRequest body
        """
        return {
            'timeQuery': {
                'dateList': {
                    'dates': [
                        self._parse_input_date (
                            input_date = input_date
                        )
                    ]
                }
            },
            'aggregationGranularity': 'DAILY',
            'metricDefinitions': metric_definitions,
            'pageSize': 200
        };


    def _query_domain_stats ( self, parent: str, body: dict, page_token: Optional [ str ] = None ) -> List [ dict ]:
        """Call GPT domainStats.query. Recursive call on pagination

        Arguments:
            parent (str): Parent uri of the domain to query
            body (dict): QueryDomainStatsRequest body
            page_token (str): Optional. Token to get next page of stats. Default : None

        Returns:
            dict[]: List of DomainStat objects
        """
        """Request body for the current page"""
        page_body = copy.deepcopy ( body );
        if ( page_token != None ):
            page_body [ 'pageToken' ] = page_token;

        """Result of the current page"""
        ret = self._service.domains ().domainStats ().query (
            parent = parent,
            body = page_body
        ).execute ();

        """Domain stats collected so far"""
        domain_stats = ret.get ( 'domainStats', [] );

        if ( ret.get ( 'nextPageToken', '' ) != '' ):
            """Domain stats from next page. Recursive call"""
            tmp = recursive_call (
                self._query_domain_stats,
                parent = parent,
                body = body,
                page_token = ret [ 'nextPageToken' ]
            );
            domain_stats += tmp;

        return domain_stats;


    def _extract_fbl_ids ( self, domain_stats: List [ dict ] ) -> List [ str ]:
        """Extract the unique feedback loop ids found in a domainStats query result

        Arguments:
            domain_stats (dict[]): List of DomainStat objects

        Returns:
            string[]: Unique feedback loop ids, in order of appearance
        """
        """Feedback loop ids already seen"""
        seen = set ();
        """Unique feedback loop ids, in order of appearance"""
        ret = [];
        
        for domain_stat in domain_stats:
            if ( domain_stat.get ( 'metric' ) != 'feedback_loop_id' ):
                continue;

            """Feedback loop id value"""
            value = extract_stat_value (
                value = domain_stat.get (
                    'value', {}
                )
            );
            
            if ( value == None ):
                continue;
            
            value = str ( value );
            if ( value in ret ):
                continue;
            
            ret.append ( value );

        return ret;


    def _gpt_get_compliance_status ( self, domain: str ) -> dict:
        """Call GPT to get the compliance status of a domain

        Arguments:
            domain (str): Domain to query

        Returns:
            dict: DomainComplianceStatus object
        """
        return self._service.domains ().getComplianceStatus (
            name = self._create_compliance_uri (
                domain = domain
            )
        ).execute ();


    def _gpt_get_domain_info ( self, domain: str, input_date: str ) -> dict:
        """Call GPT to get all infos to a domain

        Arguments:
            domain (str): Domain to query
            input_date (str): Date to query, format : YYYYMMDD

        Returns:
            dict: Process state & result
        """
        """Process state & result"""
        ret = {
            'state': True,
            'result': None
        };

        """Current domain parent uri to call"""
        parent = self._create_domain_uri (
            domain = domain
        );

        try:
            if ( self.verbose == True ):
                write_std ( [ 'Get domain info : {}'.format ( domain ) ] );

            """Domain stats : spam rate / auth / tls inbound / delivery errors / fbl"""
            domain_stats = self._query_domain_stats (
                parent = parent,
                body = self._create_query_request (
                    input_date = input_date,
                    metric_definitions = self._create_metric_definitions ()
                )
            );

            """Feedback loop ids found on this domain/date"""
            fbl_ids = self._extract_fbl_ids (
                domain_stats = domain_stats
            );

            if ( len ( fbl_ids ) > 0 ):
                ## Feedback loop spam rate, one metric per id found
                domain_stats += self._query_domain_stats (
                    parent = parent,
                    body = self._create_query_request (
                        input_date = input_date,
                        metric_definitions = self._create_fbl_metric_definitions (
                            fbl_ids = fbl_ids
                        )
                    )
                );

            ret [ 'result' ] = {
                'domainStats': domain_stats,
                'complianceStatus': self._gpt_get_compliance_status (
                    domain = domain
                )
            };
            self._stats.add_ok ();
        except HttpError as e:
            ret [ 'state' ] = False;
            """Http code"""
            code = e.resp.status;
            """Error message"""
            err = e._get_reason ().strip ();
            self._stats.add_err_http (
                code = code,
                err = err,
                domain = domain
            );

        return ret;


    def _init_parser_con ( self ) -> None:
        """Init data parser/cleaner con
        """
        self._parser = FlatData ();


    def _clean_domain_infos ( self, key: str, data: dict ) -> dict:
        """Clean domain infos

        Arguments:
            key (str): Key to identify data on cleaner
            data (dict): Domain infos to clean

        Returns:
            dict: Cleaned data
        """
        return self._parser.parse (
            key = key,
            data = data
        );


    @validate_call
    def get_domain_infos ( self, domain: str, input_date: str, print_stats: Optional [ bool ] = True ) -> dict:
        """Get infos to a domain

        Arguments:
            domain (str): Domain to query
            input_date (str): Date to query, format : YYYYMMDD
            print_stats (bool): Optional. True to display stats of the call. Defaut : True

        Returns:
            dict: Process state & domain infos
        """
        """Get domain infos"""
        ret = self._gpt_get_domain_info (
            domain = domain,
            input_date = input_date
        );

        ret [ 'domain' ] = domain;
        ret [ 'date' ] = input_date;

        if ( print_stats == True ):
            self._print_stats ();

        if ( ret [ 'state' ] == False ):
            return ret;

        ## Clean domain infos
        ret [ 'result' ] = self._clean_domain_infos (
            key = '{domain}-{date}'.format (
                domain = domain,
                date = input_date
            ),
            data = ret [ 'result' ]
        );

        ret [ 'result' ] [ 'domain' ] = domain;
        ret [ 'result' ] [ 'date' ] = input_date;

        return ret;


    def _print_stats ( self ) -> None:
        """Display calls statistics
        """
        self._stats.print_stats ();


    def _create_pool_data ( self, input_date: str ) -> List [ dict ]:
        """Create data to map call on pool with all domains

        Arguments:
            input_date (str): Date to query

        Returns:
            dict[]: List of dict with domain&input_date
        """
        return [
            { 'domain': x, 'input_date': input_date }
            for x in self._domains
        ];


    def _get_domain_infos_pool ( self, data: dict ) -> dict:
        """Abstract call to get_domain_infos from pool with data as dict

        Arguments:
            data (dict): Values domain/input_date to send to get_domain_infos

        Returns:
            dict: Result from get_domain_infos calls
        """
        return self.get_domain_infos (
            domain = data [ 'domain' ],
            input_date = data [ 'input_date' ],
            print_stats = False
        );


    def _clean_pool_returns ( self, data: List [ dict ] ) -> List [ dict ]:
        """Clean result from pool map returns : remove all state==false

        Arguments:
            data (dict[]): List of dict from pool map

        Returns:
            dict[]: List of dict from pool map with only state==true
        """
        return [
            x for x in data
            if x [ 'state' ] == True
        ];


    @validate_call
    def get_all_domains_infos ( self, input_date: str ) -> List [ dict ]:
        """Call GPT on all available domains

        Arguments:
            input_date (str): Date to query, format : YYYYMMDD

        Returns:
            list: All domain infos
        """
        """All domains infos"""
        ret = [];

        ## Get all domains
        self.get_domains ();

        """Data as dict to method args"""
        data = self._create_pool_data (
            input_date = input_date
        );

        if ( len ( data ) == 0 ):
            write_std ( [ 'Nothing to download' ] );
            return [];

        with Pool ( processes = self._pool_size ) as pool:
            ret = pool.map (
                self._get_domain_infos_pool,
                data
            );

        ## Clean result
        ret = self._clean_pool_returns (
            data = ret
        );

        self._print_stats ();

        return ret;
