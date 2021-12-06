# -*- coding: utf-8 -*-
# Copyright © tandemdude 2021-present
from __future__ import annotations

__all__ = ["_NotAGeneric", "_SingleArgBase"]

import abc
import typing as t

T = t.TypeVar("T")


class _NotAGeneric(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, item: t.Any) -> t.Any:
        ...


class _SingleArgBase(_NotAGeneric, t.Generic[T], abc.ABC):
    def __init__(self, val: t.Optional[T] = None) -> None:
        self.val = val

    def __getitem__(self, item: T) -> _SingleArgBase[T]:
        return self.__class__(item)
