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

from . import base
from . import basic
from . import executable
from . import options

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


class _Parser(base._SingleArgBase[t.Type[lightbulb.BaseParser]]):
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

        if executable._Executes in items:

            async def _wrapper(
                ctx: lightbulb.Context, *args: t.Any, _callback: _CommandCallbackT, **kwargs: t.Any
            ) -> None:
                res = _callback(ctx, *args, **kwargs)
                if inspect.iscoroutine(res):
                    await res

            callback = functools.partial(_wrapper, _callback=items[executable._Executes].val)
        else:

            async def callback(_: lightbulb.Context) -> None:
                return

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
"""The command type(s) the enclosing command implements.
Similar to lightbulb's :obj:`lightbulb.decorators.implements` decorator.

Required Parameters:
    - *Type[:obj:`lightbulb.commands.base.Command`] one or more command types for the enclosing command.

Example:

    .. code-block:: python
    
        impl = Implements[lightbulb.SlashCommand, lightbulb.PrefixCommand]
"""
Checks = _Checks()
"""The check object(s) to apply to the enclosing command.
Similar to lightbulb's :obj:`lightbulb.decorators.add_checks` decorator.

Required Parameters:
    - *:obj:`lightbulb.checks.Check` one or more checks to apply to the enclosing command.

Example:

    .. code-block:: python
    
        checks = Checks[lightbulb.guild_only, lightbulb.owner_only]
"""
ErrorHandler = _ErrorHandler()
"""The error handler function to use for the enclosing command.
Similar to lightbulb's :obj:`lightbulb.commands.base.CommandLike.set_error_handler` decorator.

Required Parameters:
    - Asyncronous function to use as the error handler for the enclosing command.

Example:
    
    .. code-block:: python
    
        async def _handler(event: lightbulb.CommandErrorEvent):
            ...
        
        handler = ErrorHandler[_handler]
"""
Aliases = _Aliases()
"""The aliases for the name of the enclosing command.
See :obj:`lightbulb.commands.base.CommandLike.aliases`.

Required Parameters:
    - *:obj:`str` one or more aliases for the enclosing command.

Example:

    .. code-block:: python
    
        aliases = Aliases["foo", "bar", "baz"]
"""
Guilds = _Guilds()
"""The guilds that the enclosing command will be created in.
See :obj:`lightbulb.commands.base.CommandLike.guilds`.

Required Parameters:
    - *:obj:`int` one or more guild IDs for the enclosing command to be created in.

Example:

    .. code-block:: python
        
        guilds = Guilds[1234, 5678]
"""
Subcommands = _Subcommands()
"""A container for the enclosing command's subcommands.

Required Parameters:
    - *``Command`` one or more commands to register to the enclosing command as subcommands.

Example:
    
    .. code-block:: python
    
        subcommands = Subcommands[Command[...], Command[...]]
"""
Parser = _Parser()
"""The parser class to use for the enclosing command.
See :obj:`lightbulb.commands.base.CommandLike.parser`.

Required Parameters:
    - Type[:obj:`lightbulb.BaseParser] parser class for the enclosing command.

Example:

    .. code-block:: python
        
        parser = Parser[lightbulb.Parser]
"""
CooldownManager = _CooldownManager()
"""The cooldown manager instance to use for the enclosing command.
See :obj:`lightbulb.commands.base.CommandLike.cooldown_manager`.

Required Parameters:
    - :obj:`lightbulb.cooldowns.CooldownManager` cooldown manager instance for the enclosing command.

Example:

    .. code-block:: python
    
        manager = CooldownManager[lightbulb.CooldownManager(lambda _: lightbulb.UserBucket(10, 1))]
"""
HelpGetter = _HelpGetter()
"""The long help text getter function for the enclosing command.
See :obj:`lightbulb.commands.base.CommandLike.help_getter`.

Required Parameters:
    - Syncronous function returning the long help text for the enclosing command.

Example:

    .. code-block:: python
    
        getter = HelpGetter[lambda _: "foobar"]
"""
AutoDefer = _AutoDefer()
"""Whether or not the enclosing command's response will be automatically deferred upon invocation.
See :obj:`lightbulb.commands.base.CommandLike.auto_defer`.

Required Parameters:
    - :obj:`bool` whether or not to automatically defer the response of the enclosing command.

Example:

    .. code-block:: python
    
        defer = AutoDefer[True]
"""
Ephemeral = _Ephemeral()
"""Whether or not the enclosing command's responses will be ephemeral by default.
See :obj:`lightbulb.commands.base.CommandLike.ephemeral`.

Required Parameters:
    - :obj:`bool` whether or not to send command responses as ephemeral by default.

Example:

    .. code-block:: python
    
        ephemeral = Ephemeral[True]
"""
CheckExempt = _CheckExempt()
"""The check exempt predicate to use for the enclosing command.
Similar to :obj:`lightbulb.decorators.check_exempt`.

Required Parameters:
    - Syncronous or asyncronous function to use as the enclosing command's check exempt predicate.

Example:

    .. code-block:: python
    
        exempt = CheckExempt[lambda ctx: ctx.author.id == 12345]
"""
Hidden = _Hidden()
"""Whether or not the enclosing command should be hidden from the default help command.
See :obj:`lightbulb.commands.base.CommandLike.hidden`.

Required Parameters:
    - :obj:`bool` whether or not to hide the enclosing command from the default help command.

Example:
    
    .. code-block:: python
    
        hidden = Hidden[True]
"""
InheritChecks = _InheritChecks()
"""Whether or not the enclosing command should inherit checks from the parent command group.
See :obj:`lightbulb.commands.base.CommandLike.inherit_checks`.

Required Parameters:
    :obj:`bool` whether or not the enclosing command will inherit the parent's checks.

Example:

    .. code-block:: python
    
        inherit = InheritChecks[True]
"""
Command = _Command()
"""A complex structure representing a lightbulb :obj:`~lightbulb.commands.base.CommandLike` object.
Similar to :obj:`lightbulb.decorators.command`.

Required Parameters:
    - :obj:`~.basic.Name` name of the command.
    - :obj:`~.basic.Description` description of the command.
    - :obj:`~.Implements` command types the command implements.

Optional Parameters:
    - :obj:`~.executable.Executes` the executable callback for the command.
    - :obj:`~.options.Options` options for the command.
    - :obj:`~.Checks` checks for the command.
    - :obj:`~.ErrorHandler` error handler for the command.
    - :obj:`~.Aliases` aliases for the command.
    - :obj:`~.Guilds` guilds for the command.
    - :obj:`~.Subcommands` subcommands for the command.
    - :obj:`~.Parser` parser for the command.
    - :obj:`~.CooldownManager` cooldown manager for the command.
    - :obj:`~.HelpGetter` help getter for the command.
    - :obj:`~.AutoDefer` auto defer value for the command.
    - :obj:`~.Ephemeral` ephemeral value for the command.
    - :obj:`~.CheckExempt` check exempt predicate for the command.
    - :obj:`~.Hidden` hidden value for the command.
    - :obj:`~.InheritChecks` inherit checks value for the command.

Example:
    
    .. code-block:: python
    
        cmd = Command[
            Implements[lightbulb.PrefixCommand],
            Name["foo"],
            Description["test command"],
            Executes[lambda ctx: ctx.respond("bar")]
        ]
"""
