# -*- coding: utf-8 -*-
# Copyright © tandemdude 2021-present
from __future__ import annotations

__all__ = ["Implements", "Command"]

import functools
import typing as t

import lightbulb

from wtf import base
from wtf import basic
from wtf import executable


class _Implements(base._NotAGeneric):
    def __init__(self, val: t.Optional[t.List[t.Type[lightbulb.Command]]] = None) -> None:
        self.val = val

    def __getitem__(self, item: t.Union[t.Type[lightbulb.Command], t.Tuple[t.Type[lightbulb.Command]]]):
        if issubclass(item, lightbulb.Command):
            return self.__class__([item])
        return self.__class__(list(item))


class _Command(base._NotAGeneric):
    def __getitem__(self, item: t.Any) -> lightbulb.CommandLike:
        items = {i.__class__: i for i in item}

        async def _wrapper(ctx: lightbulb.Context, *args, _callback, **kwargs) -> None:
            await _callback(ctx, *args, **kwargs)

        callback = functools.partial(_wrapper, _callback=items[executable._Executes].val)
        setattr(callback, "__cmd_types__", items[_Implements].val)

        return lightbulb.CommandLike(
            callback,
            items[basic._Name].val,
            items[basic._Description].val,
        )


Implements = _Implements()
Command = _Command()
