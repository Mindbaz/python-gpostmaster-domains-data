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
import logging;

from typing import List, Optional, Any;
from pydantic import validate_call;
from pprint import pprint;


#: Current module path
MODULE_PATH = os.path.dirname ( os.path.dirname ( os.path.abspath ( __file__ ) ) );
sys.path.insert ( 0, MODULE_PATH );
from googlepostmasterapi.logger import Logger;


class Base ( Logger ):
    """Base class with common methods
    """
    @validate_call
    def __init__ ( self, verbose: Optional [ bool ] = False ) -> None:
        """Default constructor

        Arguments:
            verbose (bool): Optional. Verbose mode. Default : False
        """
        super ().__init__ (
            verbose = verbose
        );


    @validate_call
    def extract_stat_value ( self, value: Optional [ dict ] = None ) -> Any:
        """Extract the actual scalar/list value from a GPT v2 StatisticValue object
    
        Arguments:
            value (dict): Optional. StatisticValue object from GPT v2 (doubleValue/floatValue/intValue/stringValue/stringList). Default : None
    
        Returns:
            mixed: Extracted value. None if nothing set
        """
        if ( value == None ):
            return None;
        
        if ( 'doubleValue' in value ):
            return value [ 'doubleValue' ];
        
        if ( 'floatValue' in value ):
            return value [ 'floatValue' ];
        
        if ( 'intValue' in value ):
            return int ( value [ 'intValue' ] );
        
        if ( 'stringValue' in value ):
            return value [ 'stringValue' ];
        
        if ( 'stringList' in value ):
            return value [ 'stringList' ].get ( 'values', [] );
        
        return None;
