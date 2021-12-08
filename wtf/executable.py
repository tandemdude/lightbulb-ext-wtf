# -*- coding: utf-8 -*-
# Copyright © tandemdude 2021-present
from __future__ import annotations

__all__ = ["Executes"]

import typing as t

import lightbulb

from wtf import base


class _Executes(base._SingleArgBase[t.Callable[[lightbulb.Context], t.Union[None, t.Coroutine[t.Any, t.Any, None]]]]):
    pass


Executes = _Executes()
"""The syncronous or asyncronous function to execute when the enclosing command is invoked.
See :obj:`lightbulb.commands.base.CommandLike.callback`.

Required Parameters:
    - Syncronous or asyncronous function to use as the callback for the enclosing command.

Example:
    
    .. code-block::python
    
        callback = Executes[lambda ctx: ctx.respond("foo")]
"""
