#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Statistics of data download from Google Postmaster Tools
# Copyright (C) 2021 Mindbaz
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

sys.path.insert ( 0, os.path.dirname ( os.path.dirname ( os.path.abspath ( __file__ ) ) ) );
from googlepostmasterapi.utils import write_std;

class Stats ( object ):
    """Process stats of GPostmaster
    
    Attributes:
        data (dict): Statistics from domains infos download
    """
    def __init__ ( self ):
        """Default constructor
        """
        """Statistics from domains infos download"""
        self.data = {
            'total': 0,
            'ok': 0,
            'err': 0,
            'err_http': {}
        };
    
    
    def add_total ( self ):
        """Increment counter : total
        """
        self.data [ 'total' ] += 1;
    
    
    def add_ok ( self ):
        """Increment counters : total + ok
        """
        self.add_total ();
        self.data [ 'ok' ] += 1;
    
    
    def add_err ( self ):
        """Increment counters : total + err
        """
        self.add_total ();
        self.data [ 'err' ] += 1;
    
    
    def add_err_http ( self, code, err, domain ):
        """Increment counters : total + err & add domain to http error data
        
        Arguments:
            code (int): Http code
            err (string): Http error message
            domain (string): Domain to add to http error
        """
        self.add_err ();
        if ( code not in self.data [ 'err_http' ] ):
            self.data [ 'err_http' ] [ code ] = { 'count': 0, 'domains': [], 'message': err };
        self.data [ 'err_http' ] [ code ] [ 'count' ] += 1;
        self.data [ 'err_http' ] [ code ] [ 'domains' ].append ( domain );
    
    
    def print_stats ( self ):
        """Display calls statistics
        
        Returns:
            bool: False if nothing to display. True otherwise
        """
        if ( self.data [ 'total' ] == 0 ):
            return False;
        
        write_std ( [
            'Total calls : {total}'.format ( total = self.data [ 'total' ] ),
            'Total calls success : {ok} ({ok_percent}%)'.format (
                ok = self.data [ 'ok' ],
                ok_percent = round ( float ( self.data [ 'ok' ] ) * 100.0 / float ( self.data [ 'total' ] ), 1 )
            ),
            'Total calls error : {err} ({err_percent}%)'.format (
                err = self.data [ 'err' ],
                err_percent = round ( float ( self.data [ 'err' ] ) * 100.0 / float ( self.data [ 'total' ] ), 1 )
            ) ] );
        
        for http_code in self.data [ 'err_http' ]:
            """Number of call errors to current http code"""
            nb_err = self.data [ 'err_http' ] [ http_code ] [ 'count' ];
            """Percent of call errors to current http code"""
            nb_err_percent = round ( float ( nb_err ) * 100.0 / float ( self.data [ 'total' ] ), 1 )
            
            write_std ( [
                'Total calls error http {http_code} : {err} ({err_percent}%)'.format (
                    http_code = http_code,
                    err = nb_err,
                    err_percent = nb_err_percent
                ),
                'Domains : {domains}'.format (
                    domains = ' / '.join ( self.data [ 'err_http' ] [ http_code ] [ 'domains' ] )
                ) ] );
        
        return True;
