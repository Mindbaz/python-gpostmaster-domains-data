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
Get a verification token to a domain
"""
import os;
import sys;
import argparse;

from pprint import pprint;


#: Current module path
MODULE_PATH = os.path.dirname ( os.path.dirname ( os.path.abspath ( __file__ ) ) );
sys.path.insert ( 0, MODULE_PATH );
from googlepostmasterapi import __version__;
from googlepostmasterapi.gpt import GPostmaster;


def run ():
    parser = argparse.ArgumentParser ( prog = 'gpt_get_domain_verify_token' );
    
    ## All arguments
    parser.add_argument ( '--token', type = str, nargs = '?', help = 'GPT token' );
    parser.add_argument ( '--domain', type = str, nargs = '?', help = 'Domain to get verification token' );
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
    
    if ( ( type ( args.domain ) is not str ) or ( args.domain.strip () == '' ) ):
        print ( 'Missing --domain file. -h to show help' );
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
    
    """Get token to verify the domain"""
    ret = g.get_domain_verify_token (
        domain = args.domain
    );
    
    print ( '\nHere is the verification token : {token}\n'.format (
        token = ret
    ) );
    
    exit ( 0 );

if __name__ == '__main__':
    run ();
