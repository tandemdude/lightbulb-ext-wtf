# -*- coding: utf-8 -*-
# Copyright © tandemdude 2021-present
from __future__ import annotations

__all__ = ["Executes"]

import typing as t

import lightbulb

from wtf import base


class _Executes(base._SingleArgBase[t.Callable[[lightbulb.Context], t.Coroutine[t.Any, t.Any, None]]]):
    pass


Executes = _Executes()
