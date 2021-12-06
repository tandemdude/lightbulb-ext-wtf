# -*- coding: utf-8 -*-
# Copyright © tandemdude 2021-present
from __future__ import annotations

__all__ = ["Name", "Description"]

from wtf import base


class _Name(base._SingleArgBase[str]):
    pass


class _Description(base._SingleArgBase[str]):
    pass


Name = _Name()
Description = _Description()
