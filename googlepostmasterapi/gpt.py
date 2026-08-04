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
import pickle;

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
from googlepostmasterapi.utils import recursive_call, write_std;


class GPostmaster ( object ):
    """Download data from Google postmaster tools
    
    Attributes:
        _uri_tpl (str): Protected. Template to create an uri to get domain infos
        _domains (string[]): Protected. All domains download from server
        _service (googleapiclient.discovery.build): Protected. Connector to GPT
        _parser (FlatData): Protected. Connector to data cleaner
        _stats (Stats): Protected. Connector to statistiques data
        _pool_size (int): Protected. Number of threads
    """
    @validate_call
    def __init__ ( self, token: str, pool_size: Optional [ int ] = 2, verbose: Optional [ bool ] = False ) -> None:
        """Default constructor
        
        Arguments:
            token (str): Absolute local file path to GPT token
            pool_size (int): Optional. Number of threads. Default : 2
            verbose (bool): Optional. Verbose mode. Default : False
        """
        """Verbose mode"""
        self.verbose = verbose;
        
        """Template to create an uri to get domain infos"""
        self._uri_tpl = 'domains/{domain}/trafficStats/{date}';
        
        """All domains download from server"""
        self._domains = [];
        
        """Number of threads"""
        self._pool_size = pool_size;
        
        self._init_resources (
            token = token
        );
    
    
    def _init_resources ( self, token: str ) -> None:
        """Init resources used by system : init service / parser / stats
        
        Arguments:
            token (str): Absolute local file path to GPT token
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
            token (str): Absolute file path to GPT token

        Returns:
            Credentials: GPT creds
        """
        with open ( token, 'rb' ) as token:
            return pickle.load ( token );
    
    
    def _init_service ( self, token: str ) -> None:
        """Init service connector
        
        Arguments:
            token (str): Absolute local file path to GPT token
        """
        """Connector to Google Postmaster Tools"""
        self._service = build (
            'gmailpostmastertools',
            'v1beta1',
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
    
    
    def _create_domain_uri ( self, domain: str, input_date: str ) -> str:
        """Create URI to a domain to query
        
        Arguments:
            domain (str): Domain to query
            input_date (str): Date to query, format : YYYYMMDD
        """
        return self._uri_tpl.format (
            domain = domain,
            date = input_date
        );
    
    
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
        
        """Current domain uri to call"""
        uri = self._create_domain_uri (
            domain = domain,
            input_date = input_date
        );
        
        try:
            if ( self.verbose == True ):
                write_std ( [ 'Get domain info : {}'.format ( domain ) ] );
            ret [ 'result' ] = self._service.domains ().trafficStats ().get ( name = uri ).execute ();
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
