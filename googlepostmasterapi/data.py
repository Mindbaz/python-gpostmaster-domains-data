#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Flattens GPT data
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
import copy;

class FlatData ( object ):
    """Clean data traffic stats from Google Postmaster Tools
    
    Attributes:
        data (dict): Data cleaned
        _data_tpl (dict): Template to clean data
        dict_reputation (dict): Assoc to translate EN reputation to int
    """
    def __init__ ( self ):
        """Default constructor
        """
        """Template to clean data"""
        self._data_tpl = {
            'user_report_spam_percent': None,
            'ips_reputations': [],
            'domain_reputation': None,
            'feedback_loop': { 'nb_row': 0, 'percent_per_uid': [] },
            'auth_use_dkim_percent': None,
            'auth_use_spf_percent': None,
            'auth_use_dmarc_percent': None,
            'tls_inbound_percent': None,
            'delivery_errors': []
        };
        
        """Data cleaned"""
        self.data = {};
        
        ## Assoc to translate EN reputation to int
        self.dict_reputation = {
            'high': 4, # i.e. : Bonne
            'medium': 3, # i.e. : Moyenne
            'low': 2, # i.e. : Plutôt mauvaise
            'bad': 1, # i.e. : Mauvaise
            'unknow': 0, # i.e. : Unknow
        };
    
    
    def _parse_user_report_spam ( self, key, value ):
        """Clean part of key : userReportedSpamRatio
        
        Arguments:
            key (string): Key to identify data
            value (float): Report ratio to convrt to percent
        
        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( value == None ):
            return False;
        
        self.data [ key ] [ 'user_report_spam_percent' ] = round ( float ( value ) * 100.0, 1 );
        return True;
    
    
    def _parse_ips_reputations ( self, key, value ):
        """Clean part of key : ipReputations
        
        Arguments:
            key (string): Key to identify data
            value (dict[]): Array with all four reputations : bad/low/medium/high
        
        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( value == None ):
            return False;
        
        """Number of ip with a reputation"""
        nb_ip = float ( sum ( int ( d.get ( 'ipCount', 0 ) ) for d in value ) );
        
        for level in value:
            if ( ( 'ipCount' in level ) == False ):
                ## No ip for this reputation
                continue;
            self.data [ key ] [ 'ips_reputations' ].append ( {
                'level': self.dict_reputation [ level [ 'reputation' ].lower () ],
                'value': round ( float ( level [ 'ipCount' ] ) * 100.0 / nb_ip, 1 ),
                'ips': ';'.join ( level [ 'sampleIps' ] )
            } );
        
        return True;
    
    
    def _parse_domain_reputations ( self, key, value ):
        """Clean part of key : domainReputation
        
        Arguments:
            key (string): Key to identify data
            value (string): Domain reputation
        
        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( value == None ):
            return False;
        self.data [ key ] [ 'domain_reputation' ] = self.dict_reputation.get ( value.lower (), 0 );
        return True;
    
    
    def _parse_feed_back_loop ( self, key, value ):
        """Clean part of key : spammyFeedbackLoops
        
        Arguments:
            key (string): Key to identify data
            value (dict[]): Array with all feedback loop splitted by uid 
        
        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( value == None ):
            return False;
        
        for fbl in value:
            if ( 'spamRatio' not in fbl ):
                ## Missing data from gpostmasters
                continue;
            
            self.data [ key ] [ 'feedback_loop' ] [ 'nb_row' ] += 1;
            self.data [ key ] [ 'feedback_loop' ] [ 'percent_per_uid' ].append ( {
                'uid': int ( fbl [ 'id' ] ),
                'spam_percent': round ( fbl [ 'spamRatio' ] * 100.0, 1 )
            } );
        
        return True;
    
    
    def _parse_use_auth ( self, key, **kargs ):
        """Clean part of keys : dkimSuccessRatio / spfSuccessRatio / dmarcSuccessRatio
        
        Arguments:
            key (string): Key to identify data
            dkim (float): DKIM ratio to convert to percent. Optional
            spf (float): SPF ratio to convert to percent. Optional
            dmarc (float): DMARC ratio to convert to percent. Optional
        
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
            self.data [ key ] [ 'auth_use_{}_percent'.format ( karg ) ] = round ( float ( kargs [ karg ] ) * 100.0, 1 );
        
        return ret;
    
    
    def _parse_crypted_inbound ( self, key, value ):
        """Clean part of key : inboundEncryptionRatio
        
        Arguments:
            key (string): Key to identify data
            value (float): Inbound encrypted ratio to convert to percent
        
        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( value == None ):
            return False;
        self.data [ key ] [ 'tls_inbound_percent' ] = round ( float ( value ) * 100.0, 1 );
        return True;
    
    
    def _parse_delivery_err ( self, key, value ):
        """Clean part of key : deliveryErrors
        
        Arguments:
            key (string): Key to identify data
            value (dict[]): Array with all delivery error ratio to convert to percent
        
        Returns:
            bool: False if no value to convert. True otherwise
        """
        if ( value == None ):
            return False;
        
        for error in value:
            if ( 'errorRatio' not in error ):
                ## No ratio to store
                continue;
            self.data [ key ] [ 'delivery_errors' ].append ( {
                'class': error [ 'errorClass' ].lower (),
                'type': error [ 'errorType' ].lower (),
                'percent': round ( error [ 'errorRatio' ] * 100.0, 1 )
            } );
        
        return True;
    
    
    def parse ( self, key, data ):
        """Parse data from GPT to a flatern version with all values
        
        Arguments:
            key (string): Key to identify data
            data (dict): Data from GPT to clean
        
        Returns:
            dict: Cleaned data from GPT
        """
        
        """Current key data"""
        self.data [ key ] = copy.deepcopy ( self._data_tpl );
        
        ## Clean : userReportedSpamRatio
        self._parse_user_report_spam ( key = key, value = data.get ( 'userReportedSpamRatio' ) );
        ## Clean : ipReputations
        self._parse_ips_reputations ( key = key, value = data.get ( 'ipReputations' ) );
        ## Clean : domainReputation
        self._parse_domain_reputations ( key = key, value = data.get ( 'domainReputation' ) );
        ## Clean : spammyFeedbackLoops
        self._parse_feed_back_loop ( key = key, value = data.get ( 'spammyFeedbackLoops' ) );
        ## Clean : dkimSuccessRatio / spfSuccessRatio / dmarcSuccessRatio
        self._parse_use_auth (
            key = key,
            dkim = data.get ( 'dkimSuccessRatio' ),
            spf = data.get ( 'spfSuccessRatio' ),
            dmarc = data.get ( 'dmarcSuccessRatio' )
        );
        ## Clean : inboundEncryptionRatio
        self._parse_crypted_inbound ( key = key, value = data.get ( 'inboundEncryptionRatio' ) );
        ## Clean : deliveryErrors
        self._parse_delivery_err ( key = key, value = data.get ( 'deliveryErrors' ) );
        
        """Cleaned data from GPT"""
        ret = copy.deepcopy ( self.data [ key ] );
        
        ## Clean data
        del ( self.data [ key ] );
        
        return ret;
