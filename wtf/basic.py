# -*- coding: utf-8 -*-
# Copyright © tandemdude 2021-present
from __future__ import annotations

__all__ = ["Name", "Description", "Type"]

import typing as t

from wtf import base


class _Name(base._SingleArgBase[str]):
    pass


class _Description(base._SingleArgBase[str]):
    pass


class _Type(base._SingleArgBase[t.Any]):
    pass


Name = _Name()
Description = _Description()
Type = _Type()
