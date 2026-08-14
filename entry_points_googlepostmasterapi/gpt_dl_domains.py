#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
"""
Downloads all domains from GPT
"""
import os;
import sys;
import argparse;
import shutil;

from datetime import datetime;
from pprint import pprint;
from typing import List, Optional;


#: Current module path
MODULE_PATH = os.path.dirname ( os.path.dirname ( os.path.abspath ( __file__ ) ) );
sys.path.insert ( 0, MODULE_PATH );
from googlepostmasterapi import __version__;
from googlepostmasterapi.gpt import GPostmaster;


def display_domains ( data: List [ str ], edge: Optional [ int ] = 2 ) -> None:
    data.sort ();
    """Current terminal length to calculs number of columns"""
    terminal_length = shutil.get_terminal_size ().columns;
    """Column length based on the wider value"""
    column_length = max ( len ( v ) for v in data ) + edge;
    """Number of columns available for display"""
    nb_columns = max ( 1, terminal_length // column_length );

    sys.stdout.write ( '\n' );
    for i in range ( 0, len ( data ), nb_columns ):
        ligne = data [ i : i + nb_columns ];
        sys.stdout.write ( ''.join (
            v.ljust ( column_length )
            for v in ligne
        ) );
        sys.stdout.write ( '\n' );
    sys.stdout.write ( '\n' );
    


def run ():
    parser = argparse.ArgumentParser ( prog = 'gpt_dl_domains' );
    
    ## All arguments
    parser.add_argument ( '--token', type = str, nargs = '?', help = 'GPT token' );
    parser.add_argument ( '--verbose', action = 'store_true', help = 'Verbose mode' );
    parser.add_argument ( '--version', action = 'store_true', help = 'Display version' );
    args = parser.parse_args ();
    
    ## Display version
    
    if ( args.version == True ):
        print ( __version__ );
        exit ( 0 );
    
    ## Valid required argument
    
    if ( args.token == None or os.path.isfile ( args.token ) == False ):
        print ( 'Missing --token file. -h to show help' );
        exit ( 2 );
    
    #
    # Print args to console
    #

    if ( args.verbose == True ):
        print ( 'v v v v v v v v v v v v v v v v v v v v v' );
        print ( 'Arguments list : ' );
        for arg in sorted ( vars ( args ) ):
            print ( '{} : {}'.format ( arg.rjust ( 30 ), getattr ( args, arg ) ) );
        print ( '^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^' );
    
    ## Begin
    
    #
    # Init tool
    #

    """Parser"""
    g = GPostmaster (
        token = args.token,
        verbose = args.verbose,
    );

    """Start query api"""
    date_start = datetime.now ();
    
    g.get_domains ();
    
    print ( 'Get data in {}s'.format (
        round (
            ( datetime.now () - date_start ).total_seconds (),
            2
        )
    ) );
    
    display_domains ( g._domains );
    
    exit ( 0 );

if __name__ == '__main__':
    run ();
