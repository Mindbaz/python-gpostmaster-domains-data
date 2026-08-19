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

from pprint import pprint;
from pydantic import validate_call;
from typing import Union, List, Optional;


class LoggingFilter ( logging.Filter ):
    """Filters all messages with level < self.max_level
    
    Attributes:
        max_level (int): Max log level value
    """
    @validate_call
    def __init__ ( self, level: int ) -> None:
        """Default constructor
        
        Arguments:
            level (int): Max log level value
        """
        """Max log level value"""
        self.max_level = level;
    
    
    @validate_call ( config = dict ( arbitrary_types_allowed = True ) )
    def filter ( self, log: logging.LogRecord ) -> bool:
        """Filter a log by its level
        
        Arguments:
            log (logging.LogRecord): Log to filter
        
        Returns:
             bool: True if log level is lower than max level
        """
        return ( log.levelno < self.max_level );


class Logger ( object ):
    """Base class to manage logger & conf
    
    Attributes:
        _logger (logging.Logger): Protected. Logger
        _log_tpl (dict): Protected. All part to create log template
        verbose (bool): Verbose mode
    """
    @validate_call
    def __init__ ( self, verbose: Optional [ bool ] = False ) -> None:
        """Default constructor
        
        Arguments:
            verbose (bool): Optional. Verbose mode. Default : false
        """
        """Verbose mode"""
        self.verbose = verbose;
        
        """Log templates"""
        self._log_tpl = {
            'base': '[%(levelname)s] %(class_name)s : %(message)s',
            'ts': '%(asctime)s'
        };
        
        self._init_resources_logger ();
    
    
    def _init_resources_logger ( self ) -> None:
        """Init resources used by system : init logger
        """
        ## Init logger
        self._init_logger ();
    
    
    def _create_log_tpl ( self ) -> str:
        """Create log template
        
        Returns:
            str: Log template
        """
        """Log template"""
        ret = self._log_tpl [ 'base' ];
        
        if ( ( 'TS' in os.environ ) and ( os.environ [ 'TS' ].lower () == 'true' ) ):
            ret = "{ts} {base}".format (
                ts = self._log_tpl [ 'ts' ],
                base = ret
            );
        
        return ret;
    
    
    def _init_logger_format ( self ) -> logging.Formatter:
        """Init format template for log output
        
        Returns:
            logging.Formatter: Log template format
        """
        return logging.Formatter (
            self._create_log_tpl ()
        );
    
    
    def _log_set_format ( self, logger: logging.StreamHandler, log_format: logging.Formatter ) -> None:
        """Set logger format
        
        Arguments:
            logger (logging.StreamHandler): Instance to set format
            log_format (logging.Formatter): Log template
        """
        logger.setFormatter (
            log_format
        );
    
    
    def _log_add_filter ( self, logger: logging.StreamHandler, level: int ) -> None:
        """Add logger filter
        
        Arguments:
            logger (logging.StreamHandler): Instance to add filter
            level (int): Max level for filter
        """
        logger.addFilter (
            LoggingFilter (
                level = level
            )
        );
    
    
    def _log_set_level ( self, logger: Union [ logging.RootLogger, logging.Logger, logging.StreamHandler ], level: int ) -> None:
        """Set logger level
        
        Arguments:
            logger (logging.StreamHandler|logging.Logger|logging.RootLogger): Instance to set level
            level (int): Level
        """
        logger.setLevel (
            level
        );
    
    
    def _init_logger_stdout ( self, log_format: logging.Formatter ) -> logging.StreamHandler:
        """Create logger handler to : stdout
        
        Arguments:
            log_format (logging.Formatter): Log template
        
        Returns:
            logging.StreamHandler: Logger handler on stdout
        """
        """Handler on stdout"""
        sh = logging.StreamHandler (
            sys.stdout
        );
        
        self._log_set_format (
            logger = sh,
            log_format = log_format
        );
        
        self._log_add_filter (
            logger = sh,
            level = logging.WARNING
        );
        
        self._log_set_level (
            logger = sh,
            level = logging.DEBUG
        );
        
        return sh;
    
    
    def _init_logger_stderr ( self, log_format: logging.Formatter ) -> logging.StreamHandler:
        """Create logger handler to : stderr
        
        Arguments:
            log_format (logging.Formatter): Log template
        
        Returns:
            logging.StreamHandler: Logger handler on stderr
        """
        """Handler on stderr"""
        sh = logging.StreamHandler (
            sys.stderr
        );
        
        self._log_set_format (
            logger = sh,
            log_format = log_format
        );
        
        self._log_set_level (
            logger = sh,
            level = logging.WARNING
        );
        
        return sh;
    
    
    def _log_get_logger ( self, name: Optional [ str ] = None ) -> Union [ logging.RootLogger, logging.Logger ]:
        """Crete logger based on name
        
        Arguments:
            name (str): Optional. Name to create logger. Default : None
        
        Returns:
            logging.RootLogger|logging.Logger: RootLogger if name is undefined. Logger otherwise
        """
        return logging.getLogger (
            name
        );
    
    
    def _log_add_handler ( self, logger: Union [ logging.RootLogger, logging.Logger ], handler: logging.StreamHandler ) -> None:
        """Add logger handler
        
        Arguments:
            logger (logging.RootLogger|logging.Logger): Instance to add handler
            handler (logging.StreamHandler): Handler
        """
        logger.addHandler (
            handler
        );
    
    
    def _init_logger ( self ) -> None:
        """Init logger with all handlers
        """
        """Log template"""
        log_format = self._init_logger_format ();
        
        ## Create root logger with handlers
        
        """Root logger to set handlers"""
        root_logger = self._log_get_logger ();
        
        if ( not ( root_logger.handlers ) ):
            self._log_add_handler (
                logger = root_logger,
                handler = self._init_logger_stdout (
                    log_format = log_format
                )
            );

            self._log_add_handler (
                logger = root_logger,
                handler = self._init_logger_stderr (
                    log_format = log_format
                )
            );

        ## Create logger with min level to display
        
        """Logger"""
        self._logger = self._log_get_logger (
            name = self._get_current_class_name ()
        );
        
        self._log_set_level (
            logger = self._logger,
            level = logging.DEBUG
        );


    def _get_current_class_name ( self ) -> str:
        """Return current instanciated class name

        Returns:
            str: Class name
        """
        return self.__class__.__name__;


    @validate_call
    def write_log ( self, logs: List [ str ], force_verbose: Optional [ bool ] = False ) -> bool:
        """Write log information
        
        Arguments:
            logs (str<>): List of logs to write
            force_verbose (bool): Optional. Force verbose mode. Overload verbose class properties. Default to False
        
        Returns:
            bool: False if no verbose mode. True otherwise
        """
        """Flag to print log"""
        _print = False;
        
        if ( bool ( self.verbose ) == True ):
            _print = True;
        
        if ( force_verbose == True ):
            _print = True;
        
        if ( _print == True ):
            for log in logs:
                self._logger.info (
                    log,
                    extra = {
                        'class_name': self._get_current_class_name ()
                    }
                );
        
        return _print;
    
    
    @validate_call
    def write_error ( self, logs: List [ str ] ) -> None:
        """Write error information
        
        Arguments:
            logs (str<>): List of logs to write
        """
        for log in logs:
            self._logger.error (
                log,
                extra = {
                    'class_name': self._get_current_class_name ()
                }
            );
