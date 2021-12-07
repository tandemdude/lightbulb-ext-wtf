# -*- coding: utf-8 -*-
# Copyright © tandemdude 2021-present
from __future__ import annotations

__all__ = [
    "Implements",
    "Checks",
    "ErrorHandler",
    "Aliases",
    "Guilds",
    "Subcommands",
    "Parser",
    "CooldownManager",
    "HelpGetter",
    "AutoDefer",
    "Ephemeral",
    "CheckExempt",
    "Hidden",
    "InheritChecks",
    "Command",
]

import collections.abc
import functools
import inspect
import typing as t

import hikari
import lightbulb

from wtf import base
from wtf import basic
from wtf import executable
from wtf import options

_CommandCallbackT = t.TypeVar("_CommandCallbackT", bound=t.Callable[..., t.Coroutine[t.Any, t.Any, None]])


class _Implements(base._NotAGeneric):
    def __init__(self, val: t.Optional[t.List[t.Type[lightbulb.Command]]] = None) -> None:
        self.val = val

    def __getitem__(
        self,
        item: t.Union[t.Type[lightbulb.Command], t.Sequence[t.Type[lightbulb.Command]]],
    ) -> _Implements:
        if isinstance(item, collections.abc.Sequence):
            return self.__class__(list(item))
        return self.__class__([item])


class _Checks(base._NotAGeneric):
    def __init__(self, val: t.Optional[t.List[lightbulb.Check]] = None) -> None:
        self.val = val

    def __getitem__(self, item: t.Union[lightbulb.Check, t.Sequence[lightbulb.Check]]) -> _Checks:
        if not isinstance(item, lightbulb.Check):
            return self.__class__(list(item))
        return self.__class__([item])


class _ErrorHandler(
    base._SingleArgBase[t.Callable[[lightbulb.CommandErrorEvent], t.Coroutine[t.Any, t.Any, t.Optional[bool]]]]
):
    pass


class _Aliases(base._NotAGeneric):
    def __init__(self, val: t.Optional[t.List[str]] = None) -> None:
        self.val = val

    def __getitem__(self, item: t.Union[str, t.Sequence[str]]) -> _Aliases:
        if not isinstance(item, str):
            return self.__class__(list(item))
        return self.__class__([item])


class _Guilds(base._NotAGeneric):
    def __init__(self, val: t.Optional[t.List[int]] = None) -> None:
        self.val = val

    def __getitem__(self, item: t.Union[t.Optional[int], t.Sequence[int]]) -> _Guilds:
        if not isinstance(item, int) and item is not None:
            return self.__class__(list(item))
        if item is None:
            return self.__class__(None)
        return self.__class__([item])


class _Subcommands(base._NotAGeneric):
    def __init__(self, val: t.Optional[t.List[lightbulb.CommandLike]] = None) -> None:
        self.val = val

    def __getitem__(self, item: t.Union[lightbulb.CommandLike, t.Tuple[lightbulb.CommandLike]]) -> _Subcommands:
        if isinstance(item, tuple):
            return self.__class__(list(item))
        return self.__class__([item])


class _Parser(base._SingleArgBase[t.Type[lightbulb.utils.BaseParser]]):
    pass


class _CooldownManager(base._SingleArgBase[lightbulb.CooldownManager]):
    pass


class _HelpGetter(base._SingleArgBase[t.Callable[[lightbulb.Command, lightbulb.Context], str]]):
    pass


class _AutoDefer(base._SingleArgBase[bool]):
    pass


class _Ephemeral(base._SingleArgBase[bool]):
    pass


class _CheckExempt(
    base._SingleArgBase[t.Callable[[lightbulb.Context], t.Union[bool, t.Coroutine[t.Any, t.Any, bool]]]]
):
    pass


class _Hidden(base._SingleArgBase[bool]):
    pass


class _InheritChecks(base._SingleArgBase[bool]):
    pass


class _Command(base._NotAGeneric):
    def __getitem__(self, item: t.Any) -> lightbulb.CommandLike:
        items = {i.__class__: i for i in item}

        async def _wrapper(ctx: lightbulb.Context, *args: t.Any, _callback: _CommandCallbackT, **kwargs: t.Any) -> None:
            res = _callback(ctx, *args, **kwargs)
            if inspect.iscoroutine(res):
                await res

        callback = functools.partial(_wrapper, _callback=items[executable._Executes].val)
        setattr(callback, "__cmd_types__", items[_Implements].val)

        guilds = getattr(items.get(_Guilds), "val", hikari.UNDEFINED)
        if guilds is None:
            guilds = ()

        return lightbulb.CommandLike(
            callback,
            items[basic._Name].val,
            items[basic._Description].val,
            {o.name: o for o in getattr(items.get(options._Options), "val", [])},
            getattr(items.get(_Checks), "val", []),
            getattr(items.get(_ErrorHandler), "val", None),
            getattr(items.get(_Aliases), "val", []),
            guilds,
            getattr(items.get(_Subcommands), "val", []),
            getattr(items.get(_Parser), "val", None),
            getattr(items.get(_CooldownManager), "val", None),
            getattr(items.get(_HelpGetter), "val", None),
            getattr(items.get(_AutoDefer), "val", False),
            getattr(items.get(_Ephemeral), "val", False),
            getattr(items.get(_CheckExempt), "val", None),
            getattr(items.get(_Hidden), "val", False),
            getattr(items.get(_InheritChecks), "val", False),
        )


Implements = _Implements()
"""The command types the command implements."""
Checks = _Checks()
"""The command's checks."""
ErrorHandler = _ErrorHandler()
"""The command's error handler function."""
Aliases = _Aliases()
"""The command's aliases."""
Guilds = _Guilds()
"""The guilds that the command will be created in."""
Subcommands = _Subcommands()
"""A container for this command's subcommands."""
Parser = _Parser()
"""The command's parser class."""
CooldownManager = _CooldownManager()
"""The command's cooldown manager instance."""
HelpGetter = _HelpGetter()
"""The command's long help text getter function."""
AutoDefer = _AutoDefer()
"""Whether or not the command will be automatically deferred upon invocation."""
Ephemeral = _Ephemeral()
"""Whether or not responses from the command will be ephemeral by default."""
CheckExempt = _CheckExempt()
"""The check exempt predicate to use for this command."""
Hidden = _Hidden()
"""Whether or not the command should be hidden from the default help command."""
InheritChecks = _InheritChecks()
"""Whether or not the subcommand should inherit checks from the parent."""
Command = _Command()
"""A command."""
