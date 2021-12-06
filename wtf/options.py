# -*- coding: utf-8 -*-
# Copyright © tandemdude 2021-present
from __future__ import annotations

__all__ = ["Options", "Option"]

import typing as t

import lightbulb

from wtf import base
from wtf import basic


class _Options(base._NotAGeneric):
    def __init__(self, val: t.Optional[t.List[lightbulb.OptionLike]] = None) -> None:
        self.val = val

    def __getitem__(
        self, item: t.Union[lightbulb.OptionLike, t.Tuple[lightbulb.OptionLike]]
    ):
        if isinstance(item, lightbulb.OptionLike):
            return self.__class__([item])
        return self.__class__(list(item))


class _Option(base._NotAGeneric):
    def __getitem__(self, item: t.Any) -> lightbulb.OptionLike:
        items = {i.__class__: i for i in item}

        return lightbulb.OptionLike(
            items[basic._Name].val,
            items[basic._Description].val,
            getattr(items.get(basic._Type), "val", str),
        )


Options = _Options()
Option = _Option()
