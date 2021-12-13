# -*- coding: utf-8 -*-
# Copyright © tandemdude 2021-present
from __future__ import annotations

__all__ = ["Name", "Description"]

from . import base


class _Name(base._SingleArgBase[str]):
    pass


class _Description(base._SingleArgBase[str]):
    pass


Name = _Name()
"""The name attribute for an object.

Required Parameters:    
    - :obj:`str` value of the object's name.

Example:

    .. code-block:: python
    
        name = Name["some_name"]
"""
Description = _Description()
"""The description attribute for an object.

Required Parameters:    
    - :obj:`str` value of the object's description.

Example:

    .. code-block:: python
    
        description = Description["some description"]
"""
