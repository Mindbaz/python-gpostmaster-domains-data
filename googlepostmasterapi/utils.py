#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Utils functions
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
import sys;

from pprint import pprint;
from pydantic import validate_call;
from typing import Any, Callable, List;


@validate_call
def write_std ( logs: List [ str ] ) -> None:
    """Quick write on stdout

    Arguments:
        logs (string[]): List of log to print on stdout
    """
    for log in logs:
        sys.stdout.write ( "{}\n".format ( log ) );


@validate_call
def recursive_call ( method: Callable, *args: Any, **kargs: Any ) -> Any:
    """Method to abstract recursive call

    Arguments:
        method (string): Mehtod name to call on current instance
        args (mixed()): Arguments to send to method
        kargs (dict): Keyword arguments to send to method

    Returns:
        mixed: Method returns
    """
    return method (
        *args,
        **kargs
    );
