# -*- coding: utf-8 -*-
# Copyright © tandemdude 2021-present
from __future__ import annotations

__all__ = ["Type", "Required", "Default", "Modifier", "Value", "Choice", "Choices", "Options", "Option"]

import typing as t

import hikari
import lightbulb

from wtf import base
from wtf import basic


class _Type(base._SingleArgBase[t.Any]):
    pass


class _Required(base._SingleArgBase[bool]):
    pass


class _Default(base._SingleArgBase[t.Any]):
    pass


class _Modifier(base._SingleArgBase[lightbulb.OptionModifier]):
    pass


class _Value(base._SingleArgBase[t.Any]):
    pass


class _Choice(base._NotAGeneric):
    def __getitem__(self, item: t.Any) -> hikari.CommandChoice:
        items = {i.__class__: i for i in item}

        return hikari.CommandChoice(name=items[basic._Name].val, value=items.get(_Value, items[basic._Name]).val)


class _Choices(base._NotAGeneric):
    def __init__(self, val: t.Optional[t.List[hikari.CommandChoice]] = None) -> None:
        self.val = val

    def __getitem__(self, item: t.Union[hikari.CommandChoice, t.Tuple[hikari.CommandChoice]]):
        if isinstance(item, hikari.CommandChoice):
            return self.__class__([item])
        return self.__class__(list(item))


class _ChannelTypes(base._NotAGeneric):
    def __init__(self, val: t.Optional[t.List[hikari.ChannelType]] = None) -> None:
        self.val = val

    def __getitem__(self, item: t.Union[hikari.ChannelType, t.Tuple[hikari.ChannelType]]) -> _ChannelTypes:
        if isinstance(item, tuple):
            return self.__class__(list(item))
        return self.__class__([item])


class _Options(base._NotAGeneric):
    def __init__(self, val: t.Optional[t.List[lightbulb.OptionLike]] = None) -> None:
        self.val = val

    def __getitem__(self, item: t.Union[lightbulb.OptionLike, t.Tuple[lightbulb.OptionLike]]):
        if isinstance(item, lightbulb.OptionLike):
            return self.__class__([item])
        return self.__class__(list(item))


class _Option(base._NotAGeneric):
    def __getitem__(self, item: t.Any) -> lightbulb.OptionLike:
        items = {i.__class__: i for i in item}

        required = getattr(items.get(_Required), "val", items.get(_Default, hikari.UNDEFINED) is hikari.UNDEFINED)
        default = hikari.UNDEFINED
        if not required:
            default = getattr(items.get(_Default), "val", None)

        return lightbulb.OptionLike(
            items[basic._Name].val,
            items[basic._Description].val,
            getattr(items.get(_Type), "val", str),
            required,
            getattr(items.get(_Choices), "val", None),
            None,
            default,
            getattr(items.get(_Modifier), "val", lightbulb.OptionModifier.NONE),
        )


Type = _Type()
"""The type of the command option."""
Required = _Required()
"""Whether or not the option is required. Inferred from the default value if not provided."""
Default = _Default()
"""The default value for the option."""
Modifier = _Modifier()
"""The parsing modifier for the option."""
Value = _Value()
"""The value for the option choice."""
Choice = _Choice()
"""A choice for the option."""
Choices = _Choices()
"""Container for all the option choices."""
ChannelTypes = _ChannelTypes()
"""Channel types allowed for this option."""
Options = _Options()
"""Container for all the command options."""
Option = _Option()
"""A command option."""
